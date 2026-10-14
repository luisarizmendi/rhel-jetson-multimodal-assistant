# Repository Guidelines

## Project Structure & Module Organization

This project targets the NVIDIA Jetson Orin Nano Super with RHEL bootc and Podman Quadlets. `services/orchestrator/app/` contains the FastAPI gateway; `services/vision/app/` contains camera endpoints and TensorRT engine-cache utilities. Other `services/` directories define LLM profiles or document deferred STT/TTS components. `bootc/files/` supplies host initialization and systemd/Quadlet configuration. `config/` holds runtime environment examples, `scripts/` contains validation and maintenance tools, and `docs/` covers architecture, deployment, compatibility, and benchmarks. No dedicated test or asset directory exists.

## Build, Test, and Development Commands

- `podman build --arch arm64 -t localhost/mma-orchestrator:dev services/orchestrator` builds the gateway container; substitute `mma-vision` and `services/vision` for vision.
- `podman build --arch arm64 -t localhost/rhel-jetson-multimodal-assistant:dev .` builds the bootc host image on a suitable builder with base-image access.
- `./scripts/validate-host.sh`, `./scripts/validate-gpu.sh`, and `./scripts/validate-camera.sh /dev/video0` check target prerequisites.
- `./scripts/smoke-test.sh` queries running orchestrator and vision endpoints; it requires `curl` and `jq`.
- For gateway-only development, install `services/orchestrator/requirements.txt` in a virtual environment, then run `uvicorn app.main:app --port 8080` from `services/orchestrator/`.

Follow `docs/deployment.md` for persistent-data initialization and systemd installation.

## Coding Style & Naming Conventions

Match existing Python: four-space indentation, snake_case functions and variables, PascalCase classes, uppercase configuration constants, and type annotations where useful. Keep dependencies pinned in each service's `requirements.txt`. Shell scripts use Bash, `set -euo pipefail`, and kebab-case filenames. No formatter or linter is configured.

## Testing Guidelines

Validation currently uses hardware checks and HTTP smoke scripts; no unit-test framework or coverage threshold is configured. Run relevant checks on the target Jetson and record commands and results. Confirm response contents as well as HTTP success: vision can report camera failures or empty detections. Document hardware-dependent checks that could not run.

## Commit & Pull Request Guidelines

Git history is unavailable in this checkout. Use concise, imperative commit subjects, such as `Fix vision cache invalidation`. PRs should describe behavior changes, link relevant issues, list validation results and target-runtime versions, and update affected deployment or compatibility documentation.

## Security & Configuration

Keep weights, engines, logs, and state under `/var/lib/multimodal-assistant`, outside the bootc image. Build TensorRT engines on the target Jetson. Use runtime environment examples without committing secrets. Preserve CDI device access and existing container restrictions; do not bypass GPU failures with privileged containers.
