# STT integration boundary

STT is intentionally not enabled in the first Quadlet set. The chosen runtime will be `whisper.cpp` with a small multilingual model and VAD in front of it. Add it only after the LLM-plus-detector memory baseline is recorded, because the device has 8 GB unified memory.

Its service contract is `POST /v1/audio/transcriptions`; its model and temporary audio files belong in `/var/lib/multimodal-assistant/models/stt` and `/var/lib/multimodal-assistant/cache`.
