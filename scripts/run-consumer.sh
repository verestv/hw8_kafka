#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="twitter-consumer"
PROJECT_NAME=${PROJECT_NAME:-$(basename "$(pwd)")}
NETWORK_NAME="${PROJECT_NAME}_default"

mkdir -p output

if ! docker network inspect "${NETWORK_NAME}" >/dev/null 2>&1; then
  echo "Error: Docker network '${NETWORK_NAME}' not found."
  echo "Make sure you ran 'docker compose up -d' from this directory."
  exit 1
fi

docker run --rm \
  --name twitter-consumer-run \
  --network "${NETWORK_NAME}" \
  -v "$(pwd)/output:/app/output" \
  -e BOOTSTRAP_SERVERS="kafka:9093" \
  -e TOPIC_NAME="tweets" \
  -e OUTPUT_DIR="/app/output" \
  -e GROUP_ID="tweets-file-writer" \
  "${IMAGE_NAME}"