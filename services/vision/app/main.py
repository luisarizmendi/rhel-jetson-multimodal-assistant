import os
import time

import cv2
from fastapi import FastAPI, HTTPException

CAMERA_DEVICE = os.getenv("CAMERA_DEVICE", "/dev/video0")
latest = {"captured_at": None, "camera": CAMERA_DEVICE, "detections": [], "status": "starting"}
frame_jpeg: bytes | None = None

app = FastAPI(title="Multimodal Assistant vision", version="0.1.0")


@app.on_event("startup")
def open_camera():
    global frame_jpeg
    capture = cv2.VideoCapture(CAMERA_DEVICE, cv2.CAP_V4L2)
    if not capture.isOpened():
        latest["status"] = "camera-unavailable"
        return
    ok, frame = capture.read()
    capture.release()
    if not ok:
        latest["status"] = "camera-read-failed"
        return
    encoded, jpeg = cv2.imencode(".jpg", frame)
    if encoded:
        frame_jpeg = jpeg.tobytes()
    latest.update({"captured_at": time.time(), "status": "ready", "detections": []})


@app.get("/health")
def health():
    return {"status": latest["status"], "camera": CAMERA_DEVICE}


@app.get("/v1/detections/latest")
def detections():
    return latest


@app.get("/v1/frame/latest")
def frame():
    if frame_jpeg is None:
        raise HTTPException(503, detail="No camera frame available")
    return {"captured_at": latest["captured_at"], "jpeg_bytes": len(frame_jpeg), "note": "Frame transport endpoint is metadata-only in v0.1"}
