# Kafka Consumer Homework README

> **This branch extends [hw8_kafka master branch](https://github.com/verestv/hw8_kafka/tree/master).**
> Complete all steps from that README before proceeding here.

## What was built

This branch adds a Kafka consumer on top of the existing producer setup:

- A Python consumer that reads messages from the `tweets` topic, groups them by the minute extracted from the `created_at` field, and writes each group into a separate CSV file. File: `consumer/consumer.py`.
- A Docker image for the consumer. File: `consumer/Dockerfile`.
- Simple shell scripts to build and run the consumer container on the same Docker network as Kafka. Files: `scripts/build-consumer.sh` and `scripts/run-consumer.sh`.
- An `output/` directory where the consumer writes minute-grouped CSV files on the host machine via a bind mount.

## Architecture overview

Kafka stores all incoming messages in the `tweets` topic log. The consumer reads new messages as they arrive, parses the JSON, extracts `author_id`, `created_at`, and `text`, and writes each message into a CSV file named after the minute it was sent. The producer and consumer run as separate containers on the same Docker Compose network, communicating through the Kafka broker at `kafka:9093`.

## Step-by-step procedure

## Step 1: Ensure homework 8 is working

The Kafka broker must already be running and the `tweets` topic must exist. Confirm with:

```bash
docker compose up -d
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --list
```

## Step 2: Project tree

```txt
hw8_kafka/
├── docker-compose.yml
├── data/
│   └── sample.csv
├── producer/
│   ├── Dockerfile
│   └── producer.py
├── consumer/
│   ├── Dockerfile
│   └── consumer.py
├── output/
├── scripts/
│   ├── build.sh
│   ├── run-producer.sh
│   ├── build-consumer.sh
│   └── run-consumer.sh
├── pyproject.toml
└── uv.lock
```

## Step 4: Implement the Python consumer

The file `consumer/consumer.py`:

- connects to Kafka at `kafka:9093` using `KafkaConsumer`,
- subscribes to the `tweets` topic,
- deserializes each incoming JSON message,
- extracts `author_id`, `created_at`, and `text`,
- parses the `created_at` timestamp to determine the minute bucket,
- writes each message as a row into `/app/output/tweets_DD_MM_YYYY_HH_MM.csv`,
- writes the CSV header only if the file does not yet exist,
- runs continuously until stopped.

## Step 5: Build the consumer image

Run:

```bash
./scripts/build-consumer.sh
```

The script runs:

```bash
docker build -f consumer/Dockerfile -t twitter-consumer .
```

## Step 6: Start the consumer container

Open a terminal and run:

```bash
./scripts/run-consumer.sh
```

This runs the consumer container:

- on the same Docker Compose network as Kafka,
- with `BOOTSTRAP_SERVERS=kafka:9093`,
- with the local `output/` folder mounted into `/app/output` so generated CSV files appear on the host machine.

The consumer starts with `auto_offset_reset="latest"`, meaning it will only process new messages that arrive after it starts. **Start the consumer before the producer.**

## Step 7: Start the producer container

In a separate terminal run:

```bash
./scripts/run-producer.sh
```

The producer begins sending tweets into the `tweets` topic at 10-15 messages per second. The consumer picks them up and writes minute-grouped CSV files into `output/`.

## Step 8: Verify output files

After a few minutes check the generated files:

```bash
ls output/
head output/tweets_DD_MM_YYYY_HH_MM.csv
```

Each file contains only messages sent during that specific minute, with columns `author_id`, `created_at`, and `text`.

## Step 9: Results

In the `screenshots/` folder:
`containers_hw9.png` - running containers (Kafka + producer + consumer).
`output_and_content_of_one_file_as_example.png` - results