# ClipForge — Contexto para Claude Code

## Stack
- Python 3.11+
- `faster-whisper` — transcripción local con CUDA (modelo large-v3)
- `Ollama` en `localhost:11434` — análisis LLM con `qwen2.5:32b`
- `ffmpeg` + `moviepy` — recorte, resize, composición de vídeo
- `insightface` + `onnxruntime-gpu` — face tracking en GPU
- `Pillow` + `opencv-python` — generación de frames de subtítulos
- `Playwright` + stealth — subida automatizada a plataformas
- `Pydantic Settings` — configuración desde `.env`
- `rich` — logging estructurado en consola

## GPU
- NVIDIA, 16 GB VRAM
- Usar `device="cuda"` en faster-whisper
- Usar `providers=["CUDAExecutionProvider", "CPUExecutionProvider"]` en ONNX/insightface
- Usar `torch.cuda.is_available()` para detección; nunca forzar CPU como fallback silencioso

## LLM local
- Ollama en `localhost:11434`, modelo `qwen2.5:32b`
- Las respuestas del LLM deben ser JSON estructurado; validar con Pydantic
- Implementar reintentos (máx. 3) si el JSON está malformado
- Chunking automático para transcripciones largas (>8000 tokens estimados)

## Arquitectura
- `core/` — lógica de procesado (transcripción, análisis, vídeo, subtítulos, face tracking)
- `platforms/` — uploaders por plataforma, patrón Strategy sobre `BaseUploader`
- `utils/` — helpers transversales (logging, GPU, ficheros)
- `pipeline.py` — orquestador que encadena todas las etapas, captura excepciones por clip

## Reglas de modularidad
- **NUNCA** escribir lógica específica de plataforma fuera de `platforms/`
- **NUNCA** llamar a APIs externas de pago desde ningún módulo
- Cambiar de TikTok a Instagram/YouTube = cambiar una clase, no reescribir lógica
- Cada módulo de `core/` puede funcionar y testearse de forma independiente

## Formato de salida de clips
- Resolución: 1080×1920 (9:16)
- Codec vídeo: H.264 (`libx264` o `h264_nvenc` con CUDA)
- Codec audio: AAC, 128 kbps
- Duración máxima: 60 segundos (restricción TikTok)
- Nombrado: `{titulo_slug}_{start}_{end}.mp4`

## Manejo de errores
- Cada módulo lanza excepciones tipadas (ej. `TranscriberError`, `AnalyzerError`)
- El pipeline captura excepciones por clip y continúa con los demás
- Loguear siempre el error completo (traceback) con `rich`, nunca silenciar
- Checkpointing en `.clipforge_state.json` para reanudar sin reprocesar

## Comandos habituales
```bash
# Pipeline completo
python pipeline.py input.mp4

# Solo transcribir + analizar (sin procesar ni subir)
python pipeline.py input.mp4 --dry-run

# Sin subida a plataforma
python pipeline.py input.mp4 --no-upload

# Ver estado del checkpoint
python pipeline.py input.mp4 --status
```
