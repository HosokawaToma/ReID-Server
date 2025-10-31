import hashlib
from dataclasses import dataclass, field, InitVar

@dataclass
class EntityClient:
    id: str
    password: InitVar[str]
    hashed_password: str = field(init=False)

    def __post_init__(self, password: str):
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()
