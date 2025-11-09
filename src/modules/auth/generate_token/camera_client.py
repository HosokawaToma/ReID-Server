import time
import jwt


class ModuleAuthGenerateTokenCameraClient:
    CAMERA_CLIENT_ID_KEY_OF_PAYLOAD = "camera_client_id"
    CAMERA_ID_KEY_OF_PAYLOAD = "camera_id"
    VIEW_ID_KEY_OF_PAYLOAD = "view_id"
    EXPIRE_TIME_KEY_OF_PAYLOAD = "exp"

    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def __call__(self, id: str, camera_id: int, view_id: int) -> str:
        return jwt.encode(
            {
                self.CAMERA_CLIENT_ID_KEY_OF_PAYLOAD: id,
                self.CAMERA_ID_KEY_OF_PAYLOAD: camera_id,
                self.VIEW_ID_KEY_OF_PAYLOAD: view_id,
                self.EXPIRE_TIME_KEY_OF_PAYLOAD: time.time() + self.expire_minutes
            },
            self.secret_key,
            self.algorithm
        )
