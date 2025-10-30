from chromadb import HttpClient, ClientAPI, Collection
from typing import Optional

class DatabaseChroma:
    _client: Optional[ClientAPI] = None

    def __new__(cls, host: str, port: str, secret_token: str):
        if cls._client is None:
            cls._client = HttpClient(
                host=host,
                port=port,
                headers={
                    "X-Chroma-Token": secret_token
                }
            )
        return super().__new__(host, port, secret_token)

    def __init__(self):
        if self._client is None:
            raise ValueError("Client is not initialized")

    def __call__(self, name: str) -> Collection:
        return self._client.get_or_create_collection(name)
