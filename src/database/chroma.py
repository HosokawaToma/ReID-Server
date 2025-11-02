from chromadb import HttpClient, Collection
from chromadb.api import ClientAPI
from typing import Optional

class DatabaseChroma:
    _client: Optional[ClientAPI] = None

    def __init__(self, host: str, port: int, secret_token: str):
        if self._client is None:
            self._client = HttpClient(
                host=host,
                port=port,
                headers={
                    "X-Chroma-Token": secret_token
                }
            )

    def __call__(self, name: str) -> Collection:
        if self._client is None:
            raise ValueError("Client is not initialized")
        return self._client.get_or_create_collection(name)
