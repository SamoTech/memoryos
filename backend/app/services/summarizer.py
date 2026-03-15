import logging
from typing import List
from app.core.config import settings
from app.models.memory import Memory

logger = logging.getLogger(__name__)


class Summarizer:
    async def summarize_memory(self, content: str) -> str:
        for method in (self._ollama, self._groq, self._openai):
            try:
                result = await method(content)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"Summarizer {method.__name__} failed: {e}")
        return content[:300] + "..." if len(content) > 300 else content

    async def summarize_session(self, memories: List[Memory]) -> str:
        joined = "\n\n".join(m.content[:500] for m in memories[:20])
        return await self.summarize_memory(joined)

    async def extract_entities(self, content: str) -> dict:
        import re
        entities = {
            "people": [],
            "projects": [],
            "technologies": [],
            "decisions": [],
            "todos": [],
        }
        tech_pattern = re.compile(
            r"\b(React|Vue|Angular|Next\.js|FastAPI|Django|Flask|PostgreSQL|SQLite|"
            r"Redis|Docker|Kubernetes|Python|TypeScript|JavaScript|Rust|Go|Java|"
            r"LangChain|OpenAI|Groq|Ollama|ChromaDB|SQLAlchemy|Alembic)\b",
            re.IGNORECASE,
        )
        entities["technologies"] = list(set(tech_pattern.findall(content)))
        decision_pattern = re.compile(
            r"(?:decided to|we will|going to|will use|chose|switched to)[^.!?]*[.!?]",
            re.IGNORECASE,
        )
        entities["decisions"] = decision_pattern.findall(content)[:5]
        todo_pattern = re.compile(
            r"(?:TODO|todo|need to|should|must|have to)[^.!?]*[.!?]",
            re.IGNORECASE,
        )
        entities["todos"] = todo_pattern.findall(content)[:5]
        return entities

    async def score_importance(self, content: str) -> float:
        score = 0.5
        signals = {
            "decided": 0.2, "decision": 0.2, "important": 0.15,
            "critical": 0.2, "todo": 0.1, "bug": 0.15, "fix": 0.1,
            "deploy": 0.15, "production": 0.2, "error": 0.1,
        }
        content_lower = content.lower()
        for keyword, boost in signals.items():
            if keyword in content_lower:
                score = min(1.0, score + boost)
        length_bonus = min(0.2, len(content) / 5000)
        return min(1.0, score + length_bonus)

    async def _ollama(self, content: str) -> str:
        import httpx
        prompt = (
            f"Summarize the following in 1-2 sentences, "
            f"preserving key decisions, facts, and technical details:\n\n{content[:2000]}"
        )
        async with httpx.AsyncClient(
            base_url=settings.OLLAMA_BASE_URL, timeout=30
        ) as client:
            resp = await client.post(
                "/api/generate",
                json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False},
            )
            resp.raise_for_status()
            return resp.json()["response"].strip()

    async def _groq(self, content: str) -> str:
        if not settings.GROQ_API_KEY:
            raise RuntimeError("Groq not configured")
        import httpx
        async with httpx.AsyncClient(
            base_url="https://api.groq.com/openai/v1",
            headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
            timeout=30,
        ) as client:
            resp = await client.post(
                "/chat/completions",
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": "Summarize in 1-2 sentences, keep key facts."},
                        {"role": "user", "content": content[:2000]},
                    ],
                    "max_tokens": 150,
                },
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()

    async def _openai(self, content: str) -> str:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OpenAI not configured")
        import openai
        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        resp = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Summarize in 1-2 sentences, keep key facts."},
                {"role": "user", "content": content[:2000]},
            ],
            max_tokens=150,
        )
        return resp.choices[0].message.content.strip()


summarizer = Summarizer()
