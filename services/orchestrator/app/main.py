import asyncio
import os
from contextlib import asynccontextmanager
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

TIMEOUT = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "60"))
GENERATION_LIMIT = int(os.getenv("MAX_GENERATION_CONCURRENCY", "1"))
generation_slots = asyncio.Semaphore(GENERATION_LIMIT)


class ChatRequest(BaseModel):
    messages: list[dict[str, Any]]
    max_tokens: int = Field(default=128, ge=1, le=512)


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(title="Multimodal Assistant", version="0.1.0", lifespan=lifespan)


def service_url(name: str) -> str:
    value = os.getenv(name, "").rstrip("/")
    if not value:
        raise HTTPException(503, detail=f"{name} is not configured")
    return value


@app.get("/health")
async def health():
    configured = {k: bool(os.getenv(k)) for k in ("LLM_URL", "VISION_URL", "STT_URL", "TTS_URL")}
    return {"status": "ok", "configured_services": configured, "generation_limit": GENERATION_LIMIT}


@app.get("/v1/camera/latest")
async def latest_camera_frame():
    url = service_url("VISION_URL")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(f"{url}/v1/frame/latest")
    response.raise_for_status()
    return response.json()


@app.get("/v1/detections/latest")
async def latest_detections():
    url = service_url("VISION_URL")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        response = await client.get(f"{url}/v1/detections/latest")
    response.raise_for_status()
    return response.json()


@app.post("/v1/chat/completions")
async def chat(request: ChatRequest):
    url = service_url("LLM_URL")
    async with generation_slots:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f"{url}/v1/chat/completions", json=request.model_dump())
    response.raise_for_status()
    return response.json()
