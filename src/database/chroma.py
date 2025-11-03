from chromadb import PersistentClient, Collection
from chromadb.api import ClientAPI
from chromadb.config import Settings
from typing import Optional

class DatabaseChroma:
    _client: Optional[ClientAPI] = None

    def __init__(self):
        if self._client is None:
            self._client = PersistentClient(path="/app/storage/chroma")

    def __call__(self, name: str) -> Collection:
        if self._client is None:
            raise ValueError("Client is not initialized")
        return self._client.get_or_create_collection(name)
