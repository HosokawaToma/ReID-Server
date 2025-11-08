from dataclasses import dataclass

@dataclass
class EntityEnvironmentPostgreSQL:
    host: str
    port: str
    user: str
    password: str
    database: str
