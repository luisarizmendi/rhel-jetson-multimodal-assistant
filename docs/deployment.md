# Deployment

## First validation

Run, in order:

```bash
./scripts/validate-host.sh
./scripts/validate-gpu.sh
./scripts/validate-camera.sh /dev/video0
sudo ./scripts/prepare-persistent-data.sh
```

`validate-gpu.sh` proves CDI using the exact `nvidia.com/gpu=all` name found on this host. If it fails, do not replace the Quadlet with `Privileged=true`; capture the error and fix only the required devices/SELinux policy.

## Service build and installation

```bash
podman build --arch arm64 -t localhost/mma-orchestrator:dev services/orchestrator
podman build --arch arm64 -t localhost/mma-vision:dev services/vision
sudo install -D -m 0644 bootc/files/etc/containers/systemd/*.container /etc/containers/systemd/
sudo systemctl daemon-reload
sudo systemctl enable --now multimodal-orchestrator.service multimodal-vision.service
./scripts/smoke-test.sh
```

## Engine recovery

Changing a model is sufficient to select a new engine due to the model hash. To reclaim space or force a rebuild:

```bash
sudo ./scripts/rebuild-engines.sh vision
sudo systemctl restart multimodal-vision.service
```

## Bootc build

```bash
podman build --arch arm64 -t localhost/rhel-jetson-multimodal-assistant:dev .
```

Use the reference repository's existing publishing and installer workflow for producing the deployable artifact. Do not embed application model weights or `/var/lib/multimodal-assistant` in the image.
