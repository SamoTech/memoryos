"""Auto-tag + entity extraction helpers."""
from __future__ import annotations

import re
from typing import List

_TECH_KEYWORDS = [
    "python", "javascript", "typescript", "react", "nextjs", "fastapi",
    "django", "flask", "postgres", "sqlite", "redis", "docker", "kubernetes",
    "langchain", "openai", "ollama", "groq", "supabase", "vercel", "tailwind",
    "prisma", "graphql", "rest", "api", "llm", "embedding", "chroma", "pinecone",
    "zustand", "redux", "vite", "webpack", "git", "github", "ci", "cd",
]

_TAG_COLORS = [
    "#6366f1", "#8b5cf6", "#ec4899", "#f43f5e", "#f97316",
    "#eab308", "#22c55e", "#14b8a6", "#06b6d4", "#3b82f6",
]


def _color_for_name(name: str) -> str:
    return _TAG_COLORS[hash(name) % len(_TAG_COLORS)]


def extract_auto_tags(content: str) -> List[str]:
    """Return lowercase tags detected from content based on keyword matching."""
    lower = content.lower()
    found = [kw for kw in _TECH_KEYWORDS if re.search(rf"\b{re.escape(kw)}\b", lower)]
    return list(dict.fromkeys(found))  # deduplicate preserving order


def score_importance(content: str, entities: dict) -> float:
    """Heuristic importance score between 0.0 and 1.0."""
    score = 0.3  # baseline

    # Length bonus: longer = more detail
    length = len(content)
    score += min(0.2, length / 5000)

    # Entity richness bonus
    total_entities = sum(
        len(v) for v in entities.values() if isinstance(v, list)
    )
    score += min(0.2, total_entities * 0.02)

    # Decision/todo bonus — high signal
    if entities.get("decisions"):
        score += 0.15
    if entities.get("todos"):
        score += 0.1

    # Code block bonus
    if "```" in content or "def " in content or "function " in content:
        score += 0.1

    return round(min(score, 1.0), 4)
