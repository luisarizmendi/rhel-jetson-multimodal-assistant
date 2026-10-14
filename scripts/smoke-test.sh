#!/usr/bin/env bash
set -euo pipefail
curl --fail --silent --show-error http://127.0.0.1:8080/health | jq .
curl --fail --silent --show-error http://127.0.0.1:8082/health | jq .
curl --fail --silent --show-error http://127.0.0.1:8082/v1/detections/latest | jq .
