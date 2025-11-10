from entities.admin_client import EntityAdminClient
import time
import jwt

class ModuleAuthGenerateTokenAdminClient:
    ADMIN_CLIENT_ID_KEY_OF_PAYLOAD = "admin_client_id"
    EXPIRE_TIME_KEY_OF_PAYLOAD = "exp"
    SECONDS_TO_MINUTES = 60

    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def __call__(self, id: str) -> str:
        return jwt.encode(
            {
                self.ADMIN_CLIENT_ID_KEY_OF_PAYLOAD: id,
                self.EXPIRE_TIME_KEY_OF_PAYLOAD: time.time() + self.expire_minutes * self.SECONDS_TO_MINUTES
            },
            self.secret_key,
            self.algorithm
        )
