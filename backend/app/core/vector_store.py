import chromadb
from chromadb.config import Settings as ChromaSettings
from .config import settings


class VectorStore:
    _client: chromadb.Client = None
    _collection = None

    @classmethod
    def get_collection(cls):
        if cls._client is None:
            path = settings.DATA_DIR / "chroma"
            path.mkdir(parents=True, exist_ok=True)
            cls._client = chromadb.PersistentClient(
                path=str(path),
                settings=ChromaSettings(anonymized_telemetry=False),
            )
        if cls._collection is None:
            cls._collection = cls._client.get_or_create_collection(
                name="memories",
                metadata={"hnsw:space": "cosine"},
            )
        return cls._collection

    @classmethod
    def reset(cls):
        cls._client = None
        cls._collection = None


vector_store = VectorStore()
