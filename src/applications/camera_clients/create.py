from src.modules.authenticator.client import ModuleAuthenticatorClient
from src.entities.camera_client import EntityCameraClient
from src.modules.database.mysql.camera_clients import ModuleDatabaseMySQLCameraClients
from src.entities.environment.jwt import EntityEnvironmentJwt
from src.entities.environment.mysql import EntityEnvironmentMysql

class ApplicationCameraClientsCreate:
    def __init__(
        self,
        authenticator_client: ModuleAuthenticatorClient,
        database_camera_clients: ModuleDatabaseMySQLCameraClients,
    ):
        self.authenticator_client = authenticator_client
        self.database_camera_clients = database_camera_clients

    @classmethod
    def create(
        cls,
        environment_jwt: EntityEnvironmentJwt,
        environment_mysql: EntityEnvironmentMysql,
    ) -> "ApplicationCameraClientsCreate":
        return cls(
            authenticator_client=ModuleAuthenticatorClient(
                secret_key=environment_jwt.secret_key(),
                algorithm=environment_jwt.algorithm(),
                expire_days=environment_jwt.expire_days(),
            ),
            database_camera_clients=ModuleDatabaseMySQLCameraClients(
                host=environment_mysql.host,
                port=environment_mysql.port,
                database=environment_mysql.database,
                user=environment_mysql.user,
                password=environment_mysql.password,
            ),
        )

    def authenticate(self, authorization: str):
        self.authenticator_client.verify(authorization)

    def client_create(self, entity_camera_client: EntityCameraClient):
        self.database_camera_clients.insert(entity_camera_client)
