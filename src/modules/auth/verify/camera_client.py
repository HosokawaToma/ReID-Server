from entities.jwt.camera_client import EntityJWTCameraClient
import jwt
import time

from errors.modules.auth.verify import ErrorModulesAuthVerify

class ModuleAuthVerifyCameraClient:
    CAMERA_CLIENT_ID_KEY_OF_PAYLOAD = "camera_client_id"
    CAMERA_ID_KEY_OF_PAYLOAD = "camera_id"
    VIEW_ID_KEY_OF_PAYLOAD = "view_id"
    EXPIRE_TIME_KEY_OF_PAYLOAD = "exp"
    SECONDS_TO_MINUTES = 60

    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def __call__(self, token: str) -> EntityJWTCameraClient:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except Exception:
            raise ErrorModulesAuthVerify("Failed to decode token")
        if not payload:
            raise ErrorModulesAuthVerify("Token in missing payload")
        if not isinstance(payload, dict):
            raise ErrorModulesAuthVerify("Payload is not a dictionary")
        camera_client_id = payload.get(self.CAMERA_CLIENT_ID_KEY_OF_PAYLOAD)
        camera_id = payload.get(self.CAMERA_ID_KEY_OF_PAYLOAD)
        view_id = payload.get(self.VIEW_ID_KEY_OF_PAYLOAD)
        expire_time = payload.get(self.EXPIRE_TIME_KEY_OF_PAYLOAD)
        if camera_client_id is None:
            raise ErrorModulesAuthVerify("Payload in missing camera client id")
        if camera_id is None:
            raise ErrorModulesAuthVerify("Payload in missing camera id")
        try:
            camera_id = int(camera_id)
        except Exception:
            raise ErrorModulesAuthVerify("Camera id is not a number")
        if view_id is None:
            raise ErrorModulesAuthVerify("Payload in missing view id")
        try:
            view_id = int(view_id)
        except Exception:
            raise ErrorModulesAuthVerify("View id is not a number")
        if expire_time is None:
            raise ErrorModulesAuthVerify("Payload in missing expire time")
        try:
            expire_time = int(expire_time)
        except Exception:
            raise ErrorModulesAuthVerify("Expire time is not a number")
        if expire_time > time.time() + self.expire_minutes * self.SECONDS_TO_MINUTES:
            raise ErrorModulesAuthVerify("Token is expired")
        return EntityJWTCameraClient(camera_client_id, camera_id, view_id)
