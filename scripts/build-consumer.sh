#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="twitter-consumer"

docker build \
  -f consumer/Dockerfile \
  -t "${IMAGE_NAME}" \
  .