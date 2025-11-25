from dataclasses import dataclass

@dataclass
class EntityCameraClient:
    id: str
    camera_id: int
    view_id: int
    hashed_password: str
