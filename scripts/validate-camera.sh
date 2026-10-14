#!/usr/bin/env bash
set -euo pipefail
device="${1:-/dev/video0}"
test -c "$device"
if command -v v4l2-ctl >/dev/null; then v4l2-ctl -d "$device" --all; else echo "Install v4l-utils to inspect $device"; fi
podman run --rm --device "$device" docker.io/library/alpine:3.21 ls -l "$device"
