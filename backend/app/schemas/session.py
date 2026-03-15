from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .memory import MemoryRead


class SessionCreate(BaseModel):
    source: str = "manual"
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

    class Config:
        from_attributes = True


class SessionDetail(SessionRead):
    memories: List[MemoryRead] = []
