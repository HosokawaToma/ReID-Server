from dataclasses import dataclass

@dataclass
class EntityEnvironmentMysql:
    host: str
    port: str
    user: str
    password: str
    database: str
