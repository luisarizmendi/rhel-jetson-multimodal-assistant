# Benchmark protocol

Use one model at a time, after 10 minutes at the intended power profile. Log `tegrastats`, ambient conditions and model revision.

| Runtime/model/precision | Context | Prompt tok/s | Generate tok/s | TTFT ms | Peak RAM | Detector active | Thermal/throttle | Notes |
|---|---:|---:|---:|---:|---:|---|---|---|
| | | | | | | | | |

Run four conditions: LLM alone, detector + LLM, audio + LLM, and selected VLM frame after unloading the text LLM if needed. Never compare a TensorRT engine with a different model or quantization as if it were an apples-to-apples benchmark.
