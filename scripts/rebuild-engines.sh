#!/usr/bin/env bash
set -euo pipefail
root=/var/lib/multimodal-assistant
component="${1:-vision}"
case "$component" in vision|llm|vlm) ;; *) echo 'usage: rebuild-engines.sh [vision|llm|vlm]' >&2; exit 2;; esac
find "$root/engines/$component" -maxdepth 1 -type f \( -name '*.engine' -o -name '*.engine.json' \) -print -delete 2>/dev/null || true
echo "Removed cached $component engines. Restart the corresponding service to build a compatible engine."
