from database.mysql.models.camera_client import DatabaseMySQLModelCameraClient
import hashlib
from dataclasses import dataclass, field, InitVar

@dataclass
class EntityCameraClient:
    id: str
    camera_id: int
    view_id: int
    password: InitVar[str | None]
    hashed_password: str | None

    def __post_init__(self, password: str | None):
        if self.hashed_password is None:
            if password is None:
                raise Exception("Password is required")
            self.hashed_password = hashlib.sha256(password.encode()).hexdigest()

    def to_database_model(self):
        return DatabaseMySQLModelCameraClient(
            id=self.id,
            hashed_password=self.hashed_password,
            camera_id=self.camera_id,
            view_id=self.view_id,
        )
