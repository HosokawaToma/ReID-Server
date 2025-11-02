from dataclasses import dataclass

@dataclass
class EntityEnvironmentChroma:
    host: str
    port: int
    secret_token: str
