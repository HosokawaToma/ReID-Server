import jwt
from entities.camera_client import EntityCameraClient
from modules.authenticator.base import ModuleAuthenticatorBase
from entities.jwt.camera_client import EntityJWTCameraClient
from typing import Any

class ModuleAuthenticatorCameraClient(ModuleAuthenticatorBase):
    EXPIRE_TIME_KEY_OF_PAYLOAD = "exp"
    CAMERA_CLIENT_ID_KEY_OF_PAYLOAD = "camera_client_id"
    CAMERA_ID_KEY_OF_PAYLOAD = "camera_id"
    VIEW_ID_KEY_OF_PAYLOAD = "view_id"

    def __init__(self, secret_key: str, algorithm: str, expire_days: int):
        super().__init__(secret_key=secret_key, algorithm=algorithm, expire_days=expire_days)

    def verify(self, authorization: str) -> EntityJWTCameraClient:
        header_type, token = self._parse_authorization(authorization)
        if header_type != self.HEADER_TYPE_KEY_OF_AUTHORIZATION:
            raise Exception("Invalid authorization header type")
        payload = self._decode_token(token)
        camera_client_id, camera_id, view_id, expire_time = self._parse_payload(payload)
        if expire_time < self._get_current_time():
            raise Exception("Token expired")
        return EntityJWTCameraClient(camera_client_id, camera_id, view_id)

    def _parse_payload(self, payload: Any) -> tuple[str, int, int, int]:
        if not isinstance(payload, dict):
            raise Exception("Invalid authorization token")
        camera_client_id = payload.get(self.CAMERA_CLIENT_ID_KEY_OF_PAYLOAD)
        camera_id = payload.get(self.CAMERA_ID_KEY_OF_PAYLOAD)
        view_id = payload.get(self.VIEW_ID_KEY_OF_PAYLOAD)
        expire_time = payload.get(self.EXPIRE_TIME_KEY_OF_PAYLOAD)
        if camera_client_id is None:
            raise Exception("Invalid authorization token")
        if camera_id is None:
            raise Exception("Invalid authorization token")
        if view_id is None:
            raise Exception("Invalid authorization token")
        if expire_time is None:
            raise Exception("Invalid authorization token")
        if not isinstance(camera_client_id, str):
            raise Exception("Invalid authorization token")
        if not isinstance(camera_id, int):
            raise Exception("Invalid authorization token")
        if not isinstance(view_id, int):
            raise Exception("Invalid authorization token")
        if not isinstance(expire_time, int):
            raise Exception("Invalid authorization token")
        return camera_client_id, camera_id, view_id, expire_time

    def generate_token(self, camera_client: EntityCameraClient) -> str:
        payload = {
            self.CAMERA_CLIENT_ID_KEY_OF_PAYLOAD: camera_client.id,
            self.CAMERA_ID_KEY_OF_PAYLOAD: camera_client.camera_id,
            self.VIEW_ID_KEY_OF_PAYLOAD: camera_client.view_id,
            self.EXPIRE_TIME_KEY_OF_PAYLOAD: self._get_expire_time()
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
