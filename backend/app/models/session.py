import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String(50), nullable=False, default="manual")
    title = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)
    memory_count = Column(Integer, default=0)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime, nullable=True)
    url = Column(String(2048), nullable=True)

    memories = relationship("Memory", back_populates="session", cascade="all, delete-orphan")
