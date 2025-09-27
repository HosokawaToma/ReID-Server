from service.database.clients import ServiceDatabaseClients
from service.authentication import ServiceAuthentication
from entities.client import Client

class ApplicationLogin:
    @staticmethod
    def process(client_id: str, password: str):
        client = Client(client_id, password)
        client_model = ServiceDatabaseClients.get_client_by_id(client.id)
        if (client_model is None or client_model.hashed_password != client.hashed_password):
            return {"message": "Invalid client_id or password"}
        token = ServiceAuthentication.generate_jwt_token_for_client(client)
        return {"message": "Success", "token": token}
