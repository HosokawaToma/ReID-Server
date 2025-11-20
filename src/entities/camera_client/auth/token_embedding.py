from dataclasses import dataclass

from errors.entities.camera_client import ErrorEntitiesCameraClientAuthTokenEmbedding

@dataclass
class EntityCameraClientAuthTokenEmbedding:
    KEY_ID = "id"
    KEY_CAMERA_ID = "camera_id"
    KEY_VIEW_ID = "view_id"

    id: str
    camera_id: int
    view_id: int

    def to_dict(self) -> dict:
        return {
            self.KEY_ID: self.id,
            self.KEY_CAMERA_ID: self.camera_id,
            self.KEY_VIEW_ID: self.view_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EntityCameraClientAuthTokenEmbedding":
        id = data.get(cls.KEY_ID)
        camera_id = data.get(cls.KEY_CAMERA_ID)
        view_id = data.get(cls.KEY_VIEW_ID)
        if not id or not isinstance(id, str) \
        or not camera_id or not isinstance(camera_id, int) \
        or not view_id or not isinstance(view_id, int):
            raise ErrorEntitiesCameraClientAuthTokenEmbedding
        return cls(
            id=id,
            camera_id=camera_id,
            view_id=view_id,
        )
