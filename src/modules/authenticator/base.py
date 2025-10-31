from datetime import datetime, timezone, timedelta
import jwt

class ModuleAuthenticatorBase:
    HEADER_TYPE_KEY_OF_AUTHORIZATION = "Bearer"

    def __init__(self, secret_key: str, algorithm: str, expire_days: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_days = expire_days

    def _parse_authorization(self, authorization: str) -> tuple[str, str]:
        header_type, token = authorization.split(" ")
        if header_type != self.HEADER_TYPE_KEY_OF_AUTHORIZATION:
            raise Exception("Invalid authorization header type")
        if token is None:
            raise Exception("Invalid authorization token")
        return header_type, token

    def _decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.InvalidTokenError:
            raise Exception("Invalid authorization token")
        return payload

    def _get_current_time(self) -> int:
        return int(datetime.now(timezone.utc).timestamp())

    def _get_expire_time(self) -> int:
        return int((datetime.now(timezone.utc) + timedelta(days=self.expire_days)).timestamp())
