import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, Boolean, Float, DateTime,
    Integer, ForeignKey, Enum, JSON
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class MemorySource(str, enum.Enum):
    chatgpt = "chatgpt"
    claude = "claude"
    gemini = "gemini"
    cursor = "cursor"
    manual = "manual"
    api = "api"
    cli = "cli"


class Memory(Base):
    __tablename__ = "memories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    embedding_id = Column(String(36), nullable=True, index=True)
    source = Column(Enum(MemorySource), nullable=False, default=MemorySource.manual)
    session_id = Column(String(36), ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True, index=True)
    entities = Column(JSON, nullable=True)
    importance_score = Column(Float, default=0.5)
    is_pinned = Column(Boolean, default=False)
    is_forgotten = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    accessed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    access_count = Column(Integer, default=0)

    session = relationship("Session", back_populates="memories")
    tags = relationship("Tag", secondary="memory_tags", back_populates="memories")
