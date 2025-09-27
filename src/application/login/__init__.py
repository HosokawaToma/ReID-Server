from fastapi import FastAPI

from entities.client import Client
from service.authentication import ServiceAuthentication
from service.database.clients import ServiceDatabaseClients


class ApplicationLogin:
    @staticmethod
    def setup(fastapi_app: FastAPI):
        fastapi_app.add_api_route(
            "/login", ApplicationLogin.endpoint, methods=["POST"])

    @staticmethod
    def endpoint(client_id: str, password: str):
        client = Client(client_id, password)
        client_model = ServiceDatabaseClients.get_client_by_id(client.id)
        if (client_model is None or client_model.hashed_password != client.hashed_password):
            return {"message": "Invalid client_id or password"}
        token = ServiceAuthentication.generate_jwt_token_for_client(client)
        return {"message": "Success", "token": token}
