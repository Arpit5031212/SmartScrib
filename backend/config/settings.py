from functools import lru_cache
from pathlib import Path
from typing import ClassVar, Literal
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent

    # App metadata
    app_name: str = "SmartScribe"
    app_version: str = "0.1.0"
    environment: Literal["DEV", "PROD", "TEST"] = "DEV"
    ollama_base_url: str = "https://ollama.com"
    ollama_llm_model: str = "minimax-m2.7:cloud"
    ollama_api_key: str | None = None
    artifacts_dir: Path = BASE_DIR / "storage" / "artifacts"
    chroma_db_path: Path = BASE_DIR / "storage" / "chroma_db"
    
    @computed_field
    @property
    def debug(self) -> bool:
        return self.environment == "DEV"

    def model_post_init(self, __context) -> None:
        # Create necessary directories if they don't exist
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_db_path.mkdir(parents=True, exist_ok=True)
        if "cloud" in self.ollama_llm_model and not self.ollama_api_key:
            raise ValueError(
                "OLLAMA_API_KEY is required when using a cloud model "
                "('minimax-m2.7:cloud' detected). "
                "Get your key from https://ollama.com/settings/keys "
                "and set OLLAMA_API_KEY in your .env file."
            )

@lru_cache
def get_settings() -> Settings:
    return Settings()