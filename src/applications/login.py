from entities.client import EntityClient
from modules.database.mysql.clients import ModuleDatabaseMySQLClients
from modules.authenticator import ModuleAuthenticator
from database.mysql import DatabaseMySQL

class ApplicationLogin:
    def __init__(
        self,
        database_clients: ModuleDatabaseMySQLClients,
        authenticator: ModuleAuthenticator,
        ):
        self.database_clients = database_clients
        self.authenticator = authenticator

    @classmethod
    def create(cls, jwt_secret_key: str, jwt_algorithm: str, mysql_engine_url: str) -> "ApplicationLogin":
        return cls(
            database_clients=ModuleDatabaseMySQLClients(DatabaseMySQL(engine_url=mysql_engine_url)),
            authenticator=ModuleAuthenticator(jwt_secret_key=jwt_secret_key, jwt_algorithm=jwt_algorithm)
        )

    def login(self, client_id: str, password: str):
        client = EntityClient(client_id, password)
        database_client = self.database_clients.get_client_by_id(client.id)
        if database_client.hashed_password != client.hashed_password:
            raise Exception("Invalid client_id or password")
        return self.authenticator.generate_token_for_client(client)
