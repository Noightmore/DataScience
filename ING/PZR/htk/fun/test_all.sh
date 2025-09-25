#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="2501_test"
SCRIPT="./testt.sh"

for wav in "$TEST_DIR"/*.wav; do
  echo "=== Recognizing: $wav ==="
  $SCRIPT "$wav"
done

