import csv
import json
import os
import signal
import sys
import time
from datetime import datetime, timezone

from kafka import KafkaProducer

BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "kafka:9093")
TOPIC_NAME = os.getenv("TOPIC_NAME", "tweets")
CSV_FILE = os.getenv("CSV_FILE", "/app/data/sample.csv")
MESSAGES_PER_SECOND = float(os.getenv("MESSAGES_PER_SECOND", "12"))

SLEEP_TIME = 1.0 / MESSAGES_PER_SECOND
RUNNING = True


def handle_shutdown(signum, frame):
    global RUNNING
    RUNNING = False


signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)


producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def stream_rows():
    while RUNNING:
        with open(CSV_FILE, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not RUNNING:
                    break

                row["created_at"] = datetime.now(timezone.utc).isoformat()
                producer.send(TOPIC_NAME, value=row)

                tweet_id = row.get("tweet_id", "unknown")
                print(f"Sent tweet_id={tweet_id}")

                time.sleep(SLEEP_TIME)


try:
    stream_rows()
finally:
    producer.flush()
    producer.close()
    print("Producer stopped cleanly.")