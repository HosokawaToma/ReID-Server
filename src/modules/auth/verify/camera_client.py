from entities.jwt.camera_client import EntityJWTCameraClient
import jwt
import time

class ModuleAuthVerifyCameraClient:
    CAMERA_CLIENT_ID_KEY_OF_PAYLOAD = "camera_client_id"
    CAMERA_ID_KEY_OF_PAYLOAD = "camera_id"
    VIEW_ID_KEY_OF_PAYLOAD = "view_id"
    EXPIRE_TIME_KEY_OF_PAYLOAD = "exp"
    MINUTES_TO_SECONDS = 60

    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def __call__(self, token: str) -> EntityJWTCameraClient:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except Exception:
            raise Exception("Invalid token")
        if not payload:
            raise Exception("Invalid token")
        if not isinstance(payload, dict):
            raise Exception("Invalid token")
        camera_client_id = payload.get(self.CAMERA_CLIENT_ID_KEY_OF_PAYLOAD)
        camera_id = payload.get(self.CAMERA_ID_KEY_OF_PAYLOAD)
        view_id = payload.get(self.VIEW_ID_KEY_OF_PAYLOAD)
        expire_time = payload.get(self.EXPIRE_TIME_KEY_OF_PAYLOAD)
        if not camera_client_id:
            raise Exception("Invalid token")
        if not camera_id:
            raise Exception("Invalid token")
        try:
            camera_id = int(camera_id)
        except Exception:
            raise Exception("Invalid token")
        if not view_id:
            raise Exception("Invalid token")
        try:
            view_id = int(view_id)
        except Exception:
            raise Exception("Invalid token")
        if not expire_time:
            raise Exception("Invalid token")
        try:
            expire_time = int(expire_time)
        except Exception:
            raise Exception("Invalid token")
        if expire_time > time.time() + self.expire_minutes * self.MINUTES_TO_SECONDS:
            raise Exception("Token expired")
        return EntityJWTCameraClient(camera_client_id, camera_id, view_id)
