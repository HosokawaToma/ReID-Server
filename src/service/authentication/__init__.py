import datetime
from entities.client import Client
from entities.client_jwt_token import ClientJwtToken
from service.environment import ServiceEnvironment
import jwt

class ServiceAuthentication:
    SECRET_KEY = ServiceEnvironment.get_JWT_SECRET()
    ALGORITHM = "HS256"

    @staticmethod
    def generate_jwt_token_for_client(client: Client) -> str:
        payload = {
            "client_id": client.id,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, ServiceAuthentication.SECRET_KEY, algorithm=ServiceAuthentication.ALGORITHM)
        return token

    @staticmethod
    def verify_jwt_token_for_client(token: str) -> ClientJwtToken | None:
        try:
            payload = jwt.decode(token, ServiceAuthentication.SECRET_KEY, algorithms=[ServiceAuthentication.ALGORITHM])
        except jwt.InvalidTokenError:
            return None
        if (payload["client_id"] is None):
            return None
        token = ClientJwtToken(token, payload["client_id"])
        return token
