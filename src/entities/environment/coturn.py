from dataclasses import dataclass

@dataclass
class EntityEnvironmentCoturn:
    host: str
    port: str
    username: str
    credential: str
    secret: str
    ttl: int
