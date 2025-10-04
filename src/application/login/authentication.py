import datetime
from entities.client import Client
from entities.client_jwt_token import ClientJwtToken
import jwt


class ApplicationLoginAuthentication:
    def __init__(self, jwt_secret_key: str, jwt_algorithm: str):
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm

    def generate_jwt_token_for_client(self, client: Client) -> str:
        expire_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        payload = {
            "client_id": client.id,
            "exp": expire_time
        }
        token = jwt.encode(payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)
        return token

    def verify_jwt_token_for_client(self, token: str) -> ClientJwtToken | None:
        try:
            payload = jwt.decode(token, self.jwt_secret_key, algorithms=[self.jwt_algorithm])
        except jwt.InvalidTokenError:
            return None
        if (payload["client_id"] is None):
            return None
        token = ClientJwtToken(token, payload["client_id"])
        return token
