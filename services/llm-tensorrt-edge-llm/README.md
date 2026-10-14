# TensorRT Edge-LLM build profile

This image is a source-build staging profile, not a statement of runtime support. Run `../../scripts/validate-host.sh`, then follow the official release-specific Edge-LLM installation instructions on the Jetson. Build engines on the target and keep them under `/var/lib/multimodal-assistant/engines/llm`.

For Orin, select only FP16, INT8 or INT4 models. Do not use FP8, MXFP8, FP4 or NVFP4 checkpoints.
