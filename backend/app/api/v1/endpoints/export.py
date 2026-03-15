import json
import csv
import io
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.models.memory import Memory

router = APIRouter()


@router.get("")
async def export_memories(
    format: str = Query("json", regex="^(json|markdown|csv|obsidian)$"),
    source: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    q = select(Memory).where(Memory.is_forgotten == False).order_by(Memory.created_at.desc())
    if source:
        q = q.where(Memory.source == source)
    result = await session.execute(q)
    memories = result.scalars().all()

    if format == "json":
        data = [
            {
                "id": m.id, "content": m.content, "summary": m.summary,
                "source": m.source.value, "importance": m.importance_score,
                "created_at": m.created_at.isoformat(), "is_pinned": m.is_pinned,
                "entities": m.entities,
            }
            for m in memories
        ]
        return StreamingResponse(
            io.StringIO(json.dumps(data, indent=2)),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=memoryos-export.json"},
        )

    if format == "markdown" or format == "obsidian":
        lines = ["# MemoryOS Export\n", f"Exported: {datetime.utcnow().isoformat()}\n\n"]
        for m in memories:
            lines.append(f"## [{m.source.value}] {m.created_at.date()}\n")
            if m.summary:
                lines.append(f"**Summary:** {m.summary}\n\n")
            lines.append(m.content + "\n\n---\n\n")
        return StreamingResponse(
            io.StringIO("".join(lines)),
            media_type="text/markdown",
            headers={"Content-Disposition": "attachment; filename=memoryos-export.md"},
        )

    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "source", "content", "summary", "importance", "created_at", "is_pinned"])
        for m in memories:
            writer.writerow([
                m.id, m.source.value, m.content, m.summary or "",
                m.importance_score, m.created_at.isoformat(), m.is_pinned,
            ])
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=memoryos-export.csv"},
        )
