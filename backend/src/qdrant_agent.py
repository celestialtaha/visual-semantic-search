from qdrant_client import AsyncQdrantClient
from os import getenv

class QdrantClientSingleton:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = AsyncQdrantClient(getenv("QDRANT_URL"))
        return cls._client