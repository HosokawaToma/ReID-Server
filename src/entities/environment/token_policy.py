from dataclasses import dataclass

@dataclass
class EntityEnvironmentTokenPolicy:
    secret_key: str
    algorithm: str
    expire_minutes: int
