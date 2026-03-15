"""MemoryOS configuration via pydantic-settings."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Server
    host: str = "127.0.0.1"
    port: int = 8765
    debug: bool = False

    # Storage
    data_dir: Path = Field(default_factory=lambda: Path.home() / ".memoryos")
    db_url: Optional[str] = None

    # Embeddings
    embedding_provider: Literal["local", "openai"] = "local"
    embedding_model: str = "all-MiniLM-L6-v2"

    # Summarization
    summarizer_provider: Literal["ollama", "groq", "openai"] = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    groq_api_key: str = ""
    groq_model: str = "llama3-70b-8192"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Features
    auto_summarize: bool = True
    auto_summarize_threshold: int = 500
    importance_scoring: bool = True
    data_retention_days: int = 0  # 0 = keep forever

    # Dashboard
    dashboard_port: int = 3000

    @field_validator("data_dir", mode="before")
    @classmethod
    def expand_data_dir(cls, v: str | Path) -> Path:
        return Path(os.path.expandvars(str(v))).expanduser()

    @property
    def resolved_db_url(self) -> str:
        if self.db_url:
            return self.db_url
        db_path = self.data_dir / "memories.db"
        return f"sqlite+aiosqlite:///{db_path}"

    @property
    def chroma_path(self) -> Path:
        return self.data_dir / "chroma"

    @property
    def models_path(self) -> Path:
        return self.data_dir / "models"


settings = Settings()

# Ensure directories exist
settings.data_dir.mkdir(parents=True, exist_ok=True)
settings.chroma_path.mkdir(parents=True, exist_ok=True)
settings.models_path.mkdir(parents=True, exist_ok=True)
