"""SQLAlchemy ORM model for Memory."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
    Table,
    Column,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.tag import memory_tag_association


class MemorySource(str):
    CHATGPT = "chatgpt"
    CLAUDE = "claude"
    GEMINI = "gemini"
    CURSOR = "cursor"
    MANUAL = "manual"
    API = "api"
    CLI = "cli"


class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    embedding_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    source: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="manual",
        index=True,
    )
    session_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True, index=True
    )
    entities: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    importance_score: Mapped[float] = mapped_column(Float, default=0.5)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_forgotten: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    accessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    access_count: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    session = relationship("Session", back_populates="memories")
    tags = relationship("Tag", secondary=memory_tag_association, back_populates="memories")
