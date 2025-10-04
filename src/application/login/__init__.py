from entities.client import Client
from application.login.authentication import ApplicationLoginAuthentication
from service.database.clients import ServiceDatabaseClients


class ApplicationLogin:
    def __init__(self, jwt_secret_key: str, jwt_algorithm: str):
        self.authentication = ApplicationLoginAuthentication(jwt_secret_key, jwt_algorithm)

    def login(self, client_id: str, password: str):
        client = Client(client_id, password)
        client_model = ServiceDatabaseClients.get_client_by_id(client.id)
        if (client_model is None or client_model.hashed_password != client.hashed_password):
            return {"message": "Invalid client_id or password"}
        token = self.authentication.generate_jwt_token_for_client(client)
        return {"message": "Success", "token": token}

    def authenticate_token(self, authorization: str) -> int | None:
        header_type, token = authorization.split(" ")
        if header_type != "Bearer":
            return None
        if token is None:
            return None
        client_jwt_token = self.authentication.verify_jwt_token_for_client(token)
        if client_jwt_token is None:
            return None
        database = ServiceDatabaseClients()
        client_model = database.get_client_by_id(client_jwt_token.client_id)
        if client_model is None:
            return None
        return client_jwt_token.client_id
