from src.modules.database.mysql.clients import ModuleDatabaseMySQLClients
from src.modules.authenticator.client import ModuleAuthenticatorClient
from src.entities.environment.jwt import EntityEnvironmentJwt
from src.entities.environment.mysql import EntityEnvironmentMysql
from src.entities.client import EntityClient
from src.database.mysql import DatabaseMySQL

class ApplicationLoginClient:
    def __init__(self, authenticator_client: ModuleAuthenticatorClient, database_clients: ModuleDatabaseMySQLClients):
        self.authenticator_client = authenticator_client
        self.database_clients = database_clients

    @classmethod
    def create(cls, environment_jwt: EntityEnvironmentJwt, environment_mysql: EntityEnvironmentMysql):
        return cls(
            authenticator_client=ModuleAuthenticatorClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_days=environment_jwt.expire_days,
            ),
            database_clients=ModuleDatabaseMySQLClients(DatabaseMySQL(
                host=environment_mysql.host,
                port=environment_mysql.port,
                user=environment_mysql.user,
                password=environment_mysql.password,
                database=environment_mysql.database,
            )),
        )

    def login(self, client_id: str, password: str):
        client = EntityClient(client_id, password)
        database_client = self.database_clients.select_by_id(client.id)
        if database_client.hashed_password != client.hashed_password:
            raise Exception("Invalid client_id or password")
        return self.authenticator_client.generate_token(client)
