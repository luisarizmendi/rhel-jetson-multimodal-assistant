#!/usr/bin/env bash
set -euo pipefail
root=/var/lib/multimodal-assistant
install -d -m 0750 "$root"/{models/{llm,vlm,vision,stt,tts},engines/{llm,vlm,vision},config,data,cache,logs}
if [[ ! -e "$root/config/runtime.env" ]]; then install -m 0640 config/runtime.env.example "$root/config/runtime.env"; fi
echo "Persistent data prepared at $root"
