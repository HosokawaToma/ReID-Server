from database.mysql.models.camera_client import DatabaseMySQLModelCameraClient
import hashlib
from dataclasses import dataclass, field, InitVar

@dataclass
class EntityCameraClient:
    id: str
    password: InitVar[str]
    hashed_password: str = field(init=False)
    camera_id: int
    view_id: int

    def __post_init__(self, password: str):
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()

    def to_database_model(self):
        if not self.password and not self.hashed_password:
            raise Exception("Password or hashed password is required")
        return DatabaseMySQLModelCameraClient(
            id=self.id,
            hashed_password=self.hashed_password,
            camera_id=self.camera_id,
            view_id=self.view_id,
        )
