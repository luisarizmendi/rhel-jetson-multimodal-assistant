#!/usr/bin/env bash
set -euo pipefail
image="${1:-nvcr.io/nvidia/l4t-cuda:r39.2.1-runtime}"
nvidia-ctk cdi list | grep -qx 'nvidia.com/gpu=all'
podman run --rm --device nvidia.com/gpu=all "$image" bash -lc 'ls -l /dev/nvhost-gpu; (command -v tegrastats && timeout 2 tegrastats) || true'
