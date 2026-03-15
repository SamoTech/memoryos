"""Export / Import memories."""
from __future__ import annotations

import csv
import io
import json
from datetime import datetime, timezone
from typing import Literal, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.memory import Memory
from app.schemas.memory import MemoryCreate
from app.services.memory_service import memory_service

router = APIRouter(prefix="/export", tags=["export"])


@router.post("")
async def export_memories(
    format: Literal["json", "markdown", "csv"] = Query(default="json"),
    source: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(Memory).where(Memory.is_forgotten == False)  # noqa: E712
    if source:
        q = q.where(Memory.source == source)
    result = await db.execute(q)
    memories = result.scalars().all()

    if format == "json":
        data = [
            {
                "id": m.id,
                "content": m.content,
                "summary": m.summary,
                "source": m.source,
                "importance_score": m.importance_score,
                "created_at": m.created_at.isoformat(),
                "is_pinned": m.is_pinned,
                "entities": m.entities,
            }
            for m in memories
        ]
        content = json.dumps({"exported_at": datetime.now(timezone.utc).isoformat(), "memories": data}, indent=2)
        return StreamingResponse(
            io.StringIO(content),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=memoryos-export.json"},
        )

    if format == "markdown":
        lines = ["# MemoryOS Export\n", f"_Exported: {datetime.now(timezone.utc).date()}_\n\n"]
        for m in memories:
            lines.append(f"## {m.created_at.strftime('%Y-%m-%d %H:%M')} — {m.source}\n")
            if m.summary:
                lines.append(f"> {m.summary}\n\n")
            lines.append(f"{m.content}\n\n---\n\n")
        content = "".join(lines)
        return StreamingResponse(
            io.StringIO(content),
            media_type="text/markdown",
            headers={"Content-Disposition": "attachment; filename=memoryos-export.md"},
        )

    if format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=["id", "content", "summary", "source", "created_at", "importance_score"],
        )
        writer.writeheader()
        for m in memories:
            writer.writerow({
                "id": m.id,
                "content": m.content[:500],
                "summary": m.summary or "",
                "source": m.source,
                "created_at": m.created_at.isoformat(),
                "importance_score": m.importance_score,
            })
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=memoryos-export.csv"},
        )


@router.post("/import")
async def import_memories(
    data: dict,
    db: AsyncSession = Depends(get_db),
):
    memories_data = data.get("memories", [])
    created = []
    for item in memories_data:
        payload = MemoryCreate(
            content=item["content"],
            source=item.get("source", "manual"),
        )
        mem = await memory_service.add(db, payload)
        created.append(mem.id)
    return {"imported": len(created)}
