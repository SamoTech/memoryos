"""SQLAlchemy ORM model for Tag + association table."""
from __future__ import annotations

import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

memory_tag_association = Table(
    "memory_tags",
    Base.metadata,
    Column("memory_id", String(36), ForeignKey("memories.id", ondelete="CASCADE")),
    Column("tag_id", String(36), ForeignKey("tags.id", ondelete="CASCADE")),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    color: Mapped[str] = mapped_column(String(7), default="#6366f1")  # indigo
    memory_count: Mapped[int] = mapped_column(Integer, default=0)

    memories = relationship("Memory", secondary=memory_tag_association, back_populates="tags")
