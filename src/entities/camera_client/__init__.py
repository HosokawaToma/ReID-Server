from database.models.camera_client import DatabaseModelCameraClient
from dataclasses import dataclass

@dataclass
class EntityCameraClient:
    id: str
    camera_id: int
    view_id: int
    hashed_password: str

    def to_database_model(self):
        return DatabaseModelCameraClient(
            id=self.id,
            hashed_password=self.hashed_password,
            camera_id=self.camera_id,
            view_id=self.view_id,
        )
