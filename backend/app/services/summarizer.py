"""LLM summarizer with priority: Ollama → Groq → OpenAI."""
from __future__ import annotations

import logging
from typing import List, Optional

from app.core.config import settings
from app.models.memory import Memory

logger = logging.getLogger(__name__)


_MEMORY_SUMMARIZE_PROMPT = """
You are a memory compression assistant. Summarize the following AI conversation
excerpt into 1-2 concise sentences preserving all key facts, decisions, and
technical details. Be extremely terse.

Content:
{content}

Summary:"""

_SESSION_SUMMARIZE_PROMPT = """
Summarize this entire AI conversation session into a short paragraph (3-5 sentences).
Focus on: what the user was working on, key decisions made, technologies discussed,
and any action items.

Memories:
{memories}

Summary:"""

_ENTITY_EXTRACT_PROMPT = """
Extract structured entities from the text below.
Return ONLY valid JSON with these keys:
  people: list of person names
  projects: list of project/product names
  technologies: list of tech stack items, libraries, tools
  decisions: list of decisions made (short phrases)
  todos: list of action items / next steps

Text:
{content}

JSON:"""


class Summarizer:
    async def _call_llm(self, prompt: str) -> str:
        provider = settings.summarizer_provider
        try:
            if provider == "ollama":
                return await self._ollama(prompt)
            elif provider == "groq":
                return await self._groq(prompt)
            elif provider == "openai":
                return await self._openai(prompt)
        except Exception as exc:  # noqa: BLE001
            logger.warning("%s LLM failed: %s — trying fallback", provider, exc)
            # Fallback chain
            for fallback in ["ollama", "groq", "openai"]:
                if fallback == provider:
                    continue
                try:
                    if fallback == "ollama":
                        return await self._ollama(prompt)
                    elif fallback == "groq":
                        return await self._groq(prompt)
                    elif fallback == "openai":
                        return await self._openai(prompt)
                except Exception as fb_exc:  # noqa: BLE001
                    logger.warning("Fallback %s also failed: %s", fallback, fb_exc)
        return ""

    async def _ollama(self, prompt: str) -> str:
        import httpx
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={"model": settings.ollama_model, "prompt": prompt, "stream": False},
            )
            resp.raise_for_status()
            return resp.json()["response"].strip()

    async def _groq(self, prompt: str) -> str:
        if not settings.groq_api_key:
            raise RuntimeError("No Groq API key configured")
        from groq import AsyncGroq
        client = AsyncGroq(api_key=settings.groq_api_key)
        chat = await client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
        )
        return chat.choices[0].message.content.strip()

    async def _openai(self, prompt: str) -> str:
        if not settings.openai_api_key:
            raise RuntimeError("No OpenAI API key configured")
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        chat = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
        )
        return chat.choices[0].message.content.strip()

    async def summarize_memory(self, content: str) -> str:
        prompt = _MEMORY_SUMMARIZE_PROMPT.format(content=content[:4000])
        return await self._call_llm(prompt)

    async def summarize_session(self, memories: List[Memory]) -> str:
        joined = "\n\n---\n\n".join(m.content[:500] for m in memories[:30])
        prompt = _SESSION_SUMMARIZE_PROMPT.format(memories=joined)
        return await self._call_llm(prompt)

    async def extract_entities(self, content: str) -> dict:
        import json
        prompt = _ENTITY_EXTRACT_PROMPT.format(content=content[:3000])
        raw = await self._call_llm(prompt)
        try:
            # Strip markdown code fences if present
            raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
            return json.loads(raw)
        except Exception:  # noqa: BLE001
            return {"people": [], "projects": [], "technologies": [], "decisions": [], "todos": []}


summarizer = Summarizer()
