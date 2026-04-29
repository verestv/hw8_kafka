import csv
import json
import os
import signal
from datetime import datetime

from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "kafka:9093")
TOPIC_NAME = os.getenv("TOPIC_NAME", "tweets")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/output")
GROUP_ID = os.getenv("GROUP_ID", "tweets-file-writer")

RUNNING = True


def handle_shutdown(signum, frame):
    global RUNNING
    RUNNING = False


signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

os.makedirs(OUTPUT_DIR, exist_ok=True)

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id=GROUP_ID,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)


def build_filename(created_at_str: str) -> str:
    dt = datetime.fromisoformat(created_at_str)
    return dt.strftime("tweets_%d_%m_%Y_%H_%M.csv")


def append_row(file_path: str, row: dict):
    file_exists = os.path.exists(file_path)
    write_header = not file_exists or os.path.getsize(file_path) == 0

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["author_id", "created_at", "text"])
        if write_header:
            writer.writeheader()
        writer.writerow(row)


try:
    while RUNNING:
        for message in consumer:
            if not RUNNING:
                break

            data = message.value

            row = {
                "author_id": data.get("author_id", ""),
                "created_at": data.get("created_at", ""),
                "text": data.get("text", ""),
            }

            filename = build_filename(row["created_at"])
            file_path = os.path.join(OUTPUT_DIR, filename)

            append_row(file_path, row)
            print(f"Wrote message to {file_path}")
finally:
    consumer.close()
    print("Consumer stopped cleanly.")