from dataclasses import dataclass

@dataclass
class EntityJWTCameraClient:
    id: str
    camera_id: int
    view_id: int
