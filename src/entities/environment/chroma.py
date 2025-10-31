from dataclasses import dataclass

@dataclass
class EntityEnvironmentChroma:
    host: str
    port: str
    secret_token: str
