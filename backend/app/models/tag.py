import uuid
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

memory_tags = Table(
    "memory_tags",
    Base.metadata,
    Column("memory_id", String(36), ForeignKey("memories.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", String(36), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False, index=True)
    color = Column(String(7), default="#6366f1")
    memory_count = Column(Integer, default=0)

    memories = relationship("Memory", secondary="memory_tags", back_populates="tags")
