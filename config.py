from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:32b"

    # Whisper
    whisper_model: str = "large-v3"
    whisper_device: str = "cuda"
    whisper_compute_type: str = "float16"

    # Directorios
    output_dir: Path = Path("./output")
    temp_dir: Path = Path("./temp")

    # Clips
    clips_min_duration: int = 20
    clips_max_duration: int = 60
    clips_max_count: int = 5

    # Plataforma
    target_platform: str = "tiktok"
    tiktok_cookies_path: Path = Path("./cookies.txt")

    # Vídeo de salida
    video_width: int = 1080
    video_height: int = 1920
    video_fps: int = 30


settings = Settings()
