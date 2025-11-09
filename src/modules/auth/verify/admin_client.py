from entities.jwt.admin_client import EntityJWTAdminClient
import jwt
import time

class ModuleAuthVerifyAdminClient:
    ADMIN_CLIENT_ID_KEY_OF_PAYLOAD = "admin_client_id"
    EXPIRE_TIME_KEY_OF_PAYLOAD = "exp"

    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def __call__(self, token: str) -> EntityJWTAdminClient:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except Exception:
            raise Exception("Invalid authorization token")
        if not payload:
            raise Exception("Invalid authorization token")
        if not isinstance(payload, dict):
            raise Exception("Invalid authorization token")
        if not payload.get(self.ADMIN_CLIENT_ID_KEY_OF_PAYLOAD):
            raise Exception("Invalid authorization token")
        admin_client_id = payload.get(self.ADMIN_CLIENT_ID_KEY_OF_PAYLOAD)
        if not isinstance(admin_client_id, str):
            raise Exception("Invalid authorization token")
        if not payload.get(self.EXPIRE_TIME_KEY_OF_PAYLOAD):
            raise Exception("Invalid authorization token")
        expire_time = payload.get(self.EXPIRE_TIME_KEY_OF_PAYLOAD)
        if not isinstance(expire_time, int):
            raise Exception("Invalid authorization token")
        if expire_time < time.time() + self.expire_minutes * 60:
            raise Exception("Token expired")
        return EntityJWTAdminClient(admin_client_id)
