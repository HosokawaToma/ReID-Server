from dataclasses import dataclass

@dataclass
class EntityEnvironmentJwt:
    secret_key: str
    algorithm: str
    expire_minutes: int

