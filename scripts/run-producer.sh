#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="twitter-producer"
PROJECT_NAME=${PROJECT_NAME:-$(basename "$(pwd)")}
NETWORK_NAME="${PROJECT_NAME}_default"

if ! docker network inspect "${NETWORK_NAME}" >/dev/null 2>&1; then
  echo "Error: Docker network '${NETWORK_NAME}' not found."
  echo "Make sure you ran 'docker compose up -d' from this directory."
  exit 1
fi

docker run --rm \
  --name twitter-producer-run \
  --network "${NETWORK_NAME}" \
  -v "$(pwd)/data:/app/data:ro" \
  -e BOOTSTRAP_SERVERS="kafka:9093" \
  -e TOPIC_NAME="tweets" \
  -e CSV_FILE="/app/data/sample.csv" \
  -e MESSAGES_PER_SECOND="12" \
  "${IMAGE_NAME}"