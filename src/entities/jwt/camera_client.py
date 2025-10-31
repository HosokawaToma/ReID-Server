from dataclasses import dataclass

@dataclass
class EntityJWTCameraClient:
    camera_client_id: str
    camera_id: int
    view_id: int
