import logging
from functools import lru_cache
from typing import List
from app.core.config import settings

logger = logging.getLogger(__name__)

MODEL_CACHE_DIR = settings.DATA_DIR / "models"
MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def _get_local_model():
    from sentence_transformers import SentenceTransformer
    logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
    return SentenceTransformer(
        settings.EMBEDDING_MODEL,
        cache_folder=str(MODEL_CACHE_DIR),
    )


class EmbeddingService:
    def embed(self, text: str) -> List[float]:
        if settings.EMBEDDING_PROVIDER == "openai" and settings.OPENAI_API_KEY:
            return self._embed_openai(text)
        return self._embed_local(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if settings.EMBEDDING_PROVIDER == "openai" and settings.OPENAI_API_KEY:
            return [self._embed_openai(t) for t in texts]
        model = _get_local_model()
        return model.encode(texts, show_progress_bar=False).tolist()

    def _embed_local(self, text: str) -> List[float]:
        model = _get_local_model()
        return model.encode(text, show_progress_bar=False).tolist()

    def _embed_openai(self, text: str) -> List[float]:
        import openai
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        resp = client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return resp.data[0].embedding


embedding_service = EmbeddingService()
