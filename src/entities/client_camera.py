from database.mysql.models import DatabaseMySQLModelClientCamera
from dataclasses import dataclass

@dataclass
class EntityClientCamera:
    client_id: int
    camera_id: int
    view_id: int

    def to_database_model(self):
        return DatabaseMySQLModelClientCamera(
            client_id=self.client_id,
            camera_id=self.camera_id,
            view_id=self.view_id,
        )
