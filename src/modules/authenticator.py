import jwt
from entities.client import EntityClient
from datetime import datetime, timezone
from datetime import timedelta

class ModuleAuthenticator:
    CLIENT_ID_KEY_OF_PAYLOAD = "client_id"

    def __init__(
        self,
        jwt_secret_key: str,
        jwt_algorithm: str
    ):
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm

    def authenticate(self, authorization: str) -> EntityClient:
        header_type, token = authorization.split(" ")
        if header_type != "Bearer":
            raise Exception("Invalid authorization header type")
        if token is None:
            raise Exception("Invalid authorization token")
        return self.verify(token)

    def verify(self, token: str) -> EntityClient:
        try:
            payload = jwt.decode(token, self.jwt_secret_key, algorithms=[self.jwt_algorithm])
        except jwt.InvalidTokenError:
            raise Exception("Invalid authorization token")
        if (payload[self.CLIENT_ID_KEY_OF_PAYLOAD] is None):
            raise Exception("Invalid authorization token")
        return EntityClient(payload[self.CLIENT_ID_KEY_OF_PAYLOAD])

    def generate_token_for_client(self, client: EntityClient) -> str:
        expire_time = datetime.now(timezone.utc) + timedelta(weeks=1)
        payload = {
            "client_id": client.id,
            "exp": expire_time
        }
        token = jwt.encode(payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)
        return token
