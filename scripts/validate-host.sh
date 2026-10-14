#!/usr/bin/env bash
set -euo pipefail
failures=0
echo '== OS =='; cat /etc/os-release
echo '== Jetson BSP =='; cat /etc/nv_tegra_release 2>/dev/null || true
echo '== Kernel / architecture =='; uname -m; uname -r
echo '== Podman =='; podman --version
echo '== CDI =='; nvidia-ctk cdi list 2>/dev/null || true
echo '== CUDA compiler =='; command -v nvcc && nvcc --version || echo 'nvcc not found (Edge-LLM builds are blocked)'
echo '== TensorRT =='; (trtexec --version || find /usr -name 'libnvinfer.so*' -type f 2>/dev/null | head -20) || true
echo '== Devices =='; ls -l /dev/nvhost* /dev/video* 2>/dev/null || true
if [[ $(uname -m) != aarch64 ]]; then echo 'ERROR: expected aarch64'; failures=$((failures + 1)); fi
if ! grep -q 'Red Hat Enterprise Linux 10.2' /etc/os-release; then echo 'WARNING: expected RHEL 10.2 reference platform'; fi
if ! nvidia-ctk cdi list 2>/dev/null | grep -qx 'nvidia.com/gpu=all'; then echo 'ERROR: CDI nvidia.com/gpu=all is unavailable'; failures=$((failures + 1)); fi
if (( failures )); then echo "Validation completed with $failures blocking failure(s)."; exit 1; fi
echo 'Host validation passed. CUDA/TensorRT output above is required before enabling the Edge-LLM profile.'
