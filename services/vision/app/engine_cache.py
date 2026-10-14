import hashlib
import json
import platform
import subprocess
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def command_version(command: list[str]) -> str:
    try:
        return subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, timeout=5).strip()
    except (OSError, subprocess.SubprocessError):
        return "unavailable"


def fingerprint(model: Path, options: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": 1,
        "model_sha256": sha256(model),
        "model_name": model.name,
        "machine": platform.machine(),
        "kernel": platform.release(),
        "tensorrt": command_version(["trtexec", "--version"]),
        "cuda": command_version(["nvcc", "--version"]),
        "options": options,
    }


def engine_path(model: Path, engine_dir: Path, options: dict[str, Any]) -> Path:
    engine_dir.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(json.dumps(fingerprint(model, options), sort_keys=True).encode()).hexdigest()[:20]
    return engine_dir / f"{model.stem}-{key}.engine"


def write_manifest(engine: Path, model: Path, options: dict[str, Any]) -> Path:
    manifest = engine.with_suffix(engine.suffix + ".json")
    manifest.write_text(json.dumps(fingerprint(model, options), indent=2, sort_keys=True) + "\n")
    return manifest


def valid_engine(engine: Path, model: Path, options: dict[str, Any]) -> bool:
    manifest = engine.with_suffix(engine.suffix + ".json")
    if not engine.is_file() or not manifest.is_file():
        return False
    try:
        return json.loads(manifest.read_text()) == fingerprint(model, options)
    except (OSError, json.JSONDecodeError):
        return False
