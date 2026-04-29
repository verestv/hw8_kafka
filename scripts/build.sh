#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="twitter-producer"

docker build \
  -f producer/Dockerfile \
  -t "${IMAGE_NAME}" \
  .