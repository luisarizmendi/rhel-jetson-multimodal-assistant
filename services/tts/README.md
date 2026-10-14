# TTS integration boundary

TTS is intentionally not enabled in the first Quadlet set. The candidate is Piper with one Spanish and one English voice validated for ARM64. Its service contract is `POST /v1/audio/speech`; downloaded voices belong in `/var/lib/multimodal-assistant/models/tts`.

This is deferred until a real audio-device test verifies the required ALSA device mappings and SELinux labeling.
