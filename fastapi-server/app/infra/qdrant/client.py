from qdrant_client import QdrantClient

from app.core.config import settings


class Qdrant:
    def __init__(self) -> None:
        self._client: QdrantClient | None = None

    def connect(self) -> None:
        self._client = QdrantClient(
            url=settings.QDRANT_CLUSTER_ENDPOINT,
            api_key=settings.QDRANT_API_KEY,
        )

    def disconnect(self) -> None:
        self._client = None

    @property
    def client(self) -> QdrantClient:
        if self._client is None:
            raise RuntimeError("Qdrant client has not been initialized")
        return self._client


qdrant = Qdrant()
