# RHEL Jetson multimodal assistant

Local-first multimodal assistant for the NVIDIA Jetson Orin Nano Super (8 GB), deployed as a RHEL bootc image with Podman Quadlets.

## Status

The repository contains a buildable initial platform: bootc host image, FastAPI orchestrator, V4L2/OpenCV camera service, a TensorRT engine-cache invalidation utility, Quadlets and host/GPU/camera smoke tests. The detector execution, STT, TTS and VLM are explicitly deferred until their target-runtime/model combinations are validated. It does **not** claim that TensorRT Edge-LLM has been built on this device yet. The `llm-llama-cpp` profile is the initial fallback; Edge-LLM must pass `scripts/validate-host.sh` and its documented target build before it is enabled.

## Host confirmed on 2026-10-14

| Item | Observed value |
|---|---|
| OS | RHEL 10.2 |
| Architecture | aarch64 |
| Jetson BSP | R39.2.1 |
| Kernel | 6.12.0-211.61.1.el10_2.aarch64 |
| Podman | 5.8.2 |
| NVIDIA CDI | `nvidia.com/gpu=0`, `nvidia.com/gpu=all` |

`dpkg-query` is not applicable on RHEL. `nvcc` was not found in the supplied output, so Edge-LLM is deliberately gated on a local CUDA/TensorRT validation.

## Quick start on the Jetson

```bash
cd /home/larizmen/DATA/REPOS/codex/rhel-jetson-multimodal-assistant
./scripts/validate-host.sh
./scripts/validate-gpu.sh
./scripts/validate-camera.sh /dev/video0
sudo ./scripts/prepare-persistent-data.sh
podman build --arch arm64 -t localhost/mma-orchestrator:dev services/orchestrator
podman build --arch arm64 -t localhost/mma-vision:dev services/vision
sudo install -D -m 0644 bootc/files/etc/containers/systemd/*.container /etc/containers/systemd/
sudo systemctl daemon-reload
sudo systemctl start multimodal-orchestrator.service multimodal-vision.service
curl -fsS http://127.0.0.1:8080/health
```

For a first test without a detector model, start only the orchestrator. The vision service requires an ONNX detector at `/var/lib/multimodal-assistant/models/vision/detector.onnx` and TensorRT Python bindings in its runtime image.

## Runtime selection

The orchestrator reads `config/runtime.env`. It only calls a service when its URL is configured. Set `LLM_URL` to the selected runtime's OpenAI-compatible endpoint. Keep one generative model loaded at a time on this 8 GB unified-memory device; the VLM is intentionally not enabled in this first runtime profile.

## Build boundaries

- Build the bootc image in CI or on an aarch64 builder with access to the base image.
- Build TensorRT engines **on the target Jetson**. They are coupled to the model, TensorRT, hardware, precision and build options.
- Store weights, engines, logs and state under `/var/lib/multimodal-assistant`, never inside the bootc image.

See [docs/architecture.md](docs/architecture.md), [docs/model-compatibility.md](docs/model-compatibility.md), [docs/deployment.md](docs/deployment.md), and [docs/benchmarking.md](docs/benchmarking.md).
