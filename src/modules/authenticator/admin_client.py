from src.entities.admin_client import EntityAdminClient
from src.entities.jwt.admin_client import EntityJWTAdminClient
from src.modules.authenticator.base import ModuleAuthenticatorBase
import jwt
from typing import Any

class ModuleAuthenticatorAdminClient(ModuleAuthenticatorBase):
    EXPIRE_TIME_KEY_OF_PAYLOAD = "exp"
    ADMIN_CLIENT_ID_KEY_OF_PAYLOAD = "admin_client_id"

    def __init__(self, secret_key: str, algorithm: str, expire_days: int):
        super().__init__(secret_key=secret_key, algorithm=algorithm, expire_days=expire_days)

    def verify(self, authorization: str) -> EntityJWTAdminClient:
        header_type, token = self._parse_authorization(authorization)
        if header_type != self.HEADER_TYPE_KEY_OF_AUTHORIZATION:
            raise Exception("Invalid authorization header type")
        payload = self._decode_token(token)
        client_id, expire_time = self._parse_payload(payload)
        if expire_time < self._get_current_time():
            raise Exception("Token expired")
        return EntityJWTAdminClient(client_id)

    def _parse_payload(self, payload: Any) -> tuple[str, int]:
        if not isinstance(payload, dict):
            raise Exception("Invalid authorization token")
        client_id = payload.get(self.ADMIN_CLIENT_ID_KEY_OF_PAYLOAD)
        expire_time = payload.get(self.EXPIRE_TIME_KEY_OF_PAYLOAD)
        if client_id is None:
            raise Exception("Invalid authorization token")
        if not isinstance(client_id, str):
            raise Exception("Invalid authorization token")
        if expire_time is None:
            raise Exception("Invalid authorization token")
        if not isinstance(expire_time, int):
            raise Exception("Invalid authorization token")
        return client_id, expire_time

    def generate_token(self, admin_client: EntityAdminClient) -> str:
        payload = {
            self.ADMIN_CLIENT_ID_KEY_OF_PAYLOAD: admin_client.id,
            self.EXPIRE_TIME_KEY_OF_PAYLOAD: self._get_expire_time()
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
