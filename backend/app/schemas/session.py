"""Pydantic schemas for Session."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from app.schemas.memory import MemoryRead


class SessionCreate(BaseModel):
    source: str
    title: Optional[str] = None
    url: Optional[str] = None


class SessionRead(BaseModel):
    id: str
    source: str
    title: Optional[str]
    summary: Optional[str]
    memory_count: int
    started_at: datetime
    ended_at: Optional[datetime]
    url: Optional[str]
    memories: List[MemoryRead] = []

    model_config = {"from_attributes": True}
