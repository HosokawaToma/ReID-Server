from entities.jwt.camera_client import EntityJWTCameraClient
import jwt
import time

class ModuleAuthVerifyCameraClient:
    HEADER_TYPE_KEY_OF_AUTHORIZATION = "Bearer"
    CAMERA_CLIENT_ID_KEY_OF_PAYLOAD = "camera_client_id"
    CAMERA_ID_KEY_OF_PAYLOAD = "camera_id"
    VIEW_ID_KEY_OF_PAYLOAD = "view_id"
    EXPIRE_TIME_KEY_OF_PAYLOAD = "exp"

    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def __call__(self, authorization: str) -> EntityJWTCameraClient:
        header_type, token = authorization.split(" ")
        if not header_type:
            raise Exception("Invalid authorization header type")
        if header_type != self.HEADER_TYPE_KEY_OF_AUTHORIZATION:
            raise Exception("Invalid authorization header type")
        if not token:
            raise Exception("Invalid authorization token")
        payload = jwt.decode(token, self.secret_key,
                             algorithms=[self.algorithm])
        if not payload:
            raise Exception("Invalid authorization token")
        if not isinstance(payload, dict):
            raise Exception("Invalid authorization token")
        camera_client_id = payload.get(self.CAMERA_CLIENT_ID_KEY_OF_PAYLOAD)
        camera_id = payload.get(self.CAMERA_ID_KEY_OF_PAYLOAD)
        view_id = payload.get(self.VIEW_ID_KEY_OF_PAYLOAD)
        expire_time = payload.get(self.EXPIRE_TIME_KEY_OF_PAYLOAD)
        if not camera_client_id:
            raise Exception("Invalid authorization token")
        if not isinstance(camera_client_id, str):
            raise Exception("Invalid authorization token")
        if not camera_id:
            raise Exception("Invalid authorization token")
        if not isinstance(camera_id, int):
            raise Exception("Invalid authorization token")
        if not view_id:
            raise Exception("Invalid authorization token")
        if not isinstance(view_id, int):
            raise Exception("Invalid authorization token")
        if not expire_time:
            raise Exception("Invalid authorization token")
        if not isinstance(expire_time, int):
            raise Exception("Invalid authorization token")
        if expire_time < time.time() + self.expire_minutes * 60:
            raise Exception("Token expired")
        return EntityJWTCameraClient(camera_client_id, camera_id, view_id)
