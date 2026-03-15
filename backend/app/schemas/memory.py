"""Pydantic schemas for Memory."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TagRead(BaseModel):
    id: str
    name: str
    color: str

    model_config = {"from_attributes": True}


class MemoryCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=50_000)
    source: str = Field(default="manual")
    session_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None


class MemoryUpdate(BaseModel):
    content: Optional[str] = None
    summary: Optional[str] = None
    is_pinned: Optional[bool] = None
    tags: Optional[List[str]] = None
    importance_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class MemoryRead(BaseModel):
    id: str
    content: str
    summary: Optional[str]
    source: str
    session_id: Optional[str]
    entities: Optional[Dict[str, Any]]
    importance_score: float
    is_pinned: bool
    is_forgotten: bool
    created_at: datetime
    accessed_at: datetime
    access_count: int
    tags: List[TagRead] = []

    model_config = {"from_attributes": True}


class MemoryBulkCreate(BaseModel):
    memories: List[MemoryCreate]
    session_id: Optional[str] = None
    source: Optional[str] = None
