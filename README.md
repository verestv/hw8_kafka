# Kafka Homework README

## What was built

The project contains four main parts:

- A Kafka installation in Docker Compose using a single-node KRaft setup, where the same Kafka container acts as both broker and controller for local development. File: `docker-compose.yml`.[1]
- A Python producer that reads the CSV file with `csv.DictReader`, converts each row into JSON, updates `created_at`, and sends the record to Kafka. File: `producer/producer.py`.[2]
- A Docker image for the producer, File: `producer/Dockerfile`.[3]
- Simple shell scripts to build and run the producer container on the same Docker network as Kafka. Files: `scripts/build.sh` and `scripts/run-producer.sh`.[4]

## Architecture overview

The Kafka container is the central message broker and controller. Producers send data into topics, brokers store the messages in the topic log, and consumers are separate client processes that read those messages later.[1]

In this homework, the Python producer writes JSON messages into the `tweets` topic, and the Kafka console consumer is used only as a demonstration tool to verify that the messages arrive correctly. The console consumer prints the message value it receives, so it shows JSON because the producer sends JSON.[1]

## Step-by-step procedure

## Step 1: Initialize the Python project with uv

In the project root directory:

```bash
uv init
uv add kafka-python
```

## Step 2: Project tree

hw8_kafka/
├── docker-compose.yml
├── data/
│   └── sample.csv
├── producer/
│   ├── Dockerfile
│   └── producer.py
├── scripts/
│   ├── build.sh
│   └── run-producer.sh
├── pyproject.toml
└── uv.lock


## Step 3: Start Kafka with Docker Compose

Run:

```bash
docker compose up -d
```

## Step 4: Create the `tweets` topic

Run:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic tweets \
  --partitions 1 \
  --replication-factor 1 \
  --bootstrap-server localhost:9092
```

Verify it exists:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --list
```

## Step 5: Start the Kafka console consumer

Open a separate terminal and run:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic tweets \
  --from-beginning
```
now it waits for messages from `tweets` and prints them to the terminal.[1]

## Step 6: Implement the Python producer

The file `producer/producer.py`:

- reads rows from `data/sample.csv` with `csv.DictReader`,
- replaces `created_at` with the current timestamp,
- send each row as JSON to Kafka,
- sleep between sends to keep a rate of about 10 to 15 messages per second,
- loop continuously so the stream can run for several minutes.


## Step 7: Build the producer image from DockerFile

Run:

```bash
./scripts/build.sh
```

The script runs:

```bash
docker build -f producer/Dockerfile -t twitter-producer .
```


## Step 8: Run the producer container

Run:

```bash
./scripts/run-producer.sh
```

This script runs the producer container:

- on the same Docker Compose network as Kafka,
- with `BOOTSTRAP_SERVERS=kafka:9093`,
- with the `data/` folder where our csvs reside, mounted into `/app/data`.


## Step 10: Results
at screenshots folder: 
`containers.png` - running containers
`running_programm_and_kafka_cli_output.png` demostration of reading the topic contents using the Kafka console client.
