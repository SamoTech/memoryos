from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional


class Settings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8765
    DEBUG: bool = False

    DATA_DIR: Path = Path.home() / ".memoryos"
    DB_URL: Optional[str] = None

    EMBEDDING_PROVIDER: str = "local"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    SUMMARIZER_PROVIDER: str = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"

    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama3-70b-8192"

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    AUTO_SUMMARIZE: bool = True
    AUTO_SUMMARIZE_THRESHOLD: int = 500
    IMPORTANCE_SCORING: bool = True
    DATA_RETENTION_DAYS: int = 0

    DASHBOARD_PORT: int = 3000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def model_post_init(self, __context):
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        if self.DB_URL is None:
            object.__setattr__(
                self,
                "DB_URL",
                f"sqlite+aiosqlite:///{self.DATA_DIR}/memories.db",
            )


settings = Settings()
