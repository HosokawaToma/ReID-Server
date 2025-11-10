from errors.modules.auth.verify import ErrorModulesAuthVerify
from entities.jwt.admin_client import EntityJWTAdminClient
import jwt
import time

class ModuleAuthVerifyAdminClient:
    ADMIN_CLIENT_ID_KEY_OF_PAYLOAD = "admin_client_id"
    EXPIRE_TIME_KEY_OF_PAYLOAD = "exp"
    SECONDS_TO_MINUTES = 60

    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def __call__(self, token: str) -> EntityJWTAdminClient:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except Exception:
            raise ErrorModulesAuthVerify("Failed to decode token")
        if not payload:
            raise ErrorModulesAuthVerify("Token in missing payload")
        if not isinstance(payload, dict):
            raise ErrorModulesAuthVerify("Payload is not a dictionary")
        admin_client_id = payload.get(self.ADMIN_CLIENT_ID_KEY_OF_PAYLOAD)
        if admin_client_id is None:
            raise ErrorModulesAuthVerify("Payload in missing admin client id")
        expire_time = payload.get(self.EXPIRE_TIME_KEY_OF_PAYLOAD)
        if expire_time is None:
            raise ErrorModulesAuthVerify("Payload in missing expire time")
        try:
            expire_time = int(expire_time)
        except Exception:
            raise ErrorModulesAuthVerify("Expire time is not a number")
        if expire_time > time.time() + self.expire_minutes * self.SECONDS_TO_MINUTES:
            raise ErrorModulesAuthVerify("Token is expired")
        return EntityJWTAdminClient(admin_client_id)
