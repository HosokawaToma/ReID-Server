from database.mysql.models import DatabaseMySQLModelClient
import hashlib
from dataclasses import dataclass, field, InitVar

@dataclass
class EntityClient:
    id: str
    password: InitVar[str]
    hashed_password: str = field(init=False)

    def __post_init__(self, password: str):
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()

    def to_database_model(self):
        if not self.password and not self.hashed_password:
            raise Exception("Password or hashed password is required")
        return DatabaseMySQLModelClient(
            id=self.id,
            hashed_password=self.hashed_password,
        )
