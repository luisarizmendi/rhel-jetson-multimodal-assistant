# Runtime and model compatibility

| Component | Initial choice | State |
|---|---|---|
| Text LLM | llama.cpp CUDA, small GGUF model | baseline to validate |
| Text LLM optimized | TensorRT Edge-LLM, INT4/INT8/FP16 | experimental until target build passes |
| Detector | small YOLO ONNX → TensorRT | camera service + cache contract implemented; model runner pending |
| STT | whisper.cpp, multilingual small/base | planned |
| TTS | Piper Spanish/English | planned |
| VLM | small supported Qwen/InternVL-class checkpoint | deferred pending memory test |

Jetson Orin does not support FP8, MXFP8, FP4 or NVFP4 runtime precision in TensorRT Edge-LLM. Use FP16, INT8 or INT4 only. Model support is release-specific; record the exact upstream release, checkpoint revision and conversion settings in the engine directory beside the generated engine.
