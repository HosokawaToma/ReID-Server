from modules.authenticator.admin_client import ModuleAuthenticatorAdminClient
from entities.camera_client import EntityCameraClient
from modules.database.mysql.camera_clients import ModuleDatabaseMySQLCameraClients
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.mysql import EntityEnvironmentMysql
from database.mysql import DatabaseMySQL

class ApplicationCameraClientsCreate:
    def __init__(
        self,
        authenticator: ModuleAuthenticatorAdminClient,
        database_camera_clients: ModuleDatabaseMySQLCameraClients,
    ):
        self.authenticator = authenticator
        self.database_camera_clients = database_camera_clients

    @classmethod
    def create(
        cls,
        environment_jwt: EntityEnvironmentJwt,
        environment_mysql: EntityEnvironmentMysql,
    ) -> "ApplicationCameraClientsCreate":
        return cls(
            authenticator=ModuleAuthenticatorAdminClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_days=environment_jwt.expire_days,
            ),
            database_camera_clients=ModuleDatabaseMySQLCameraClients(
                DatabaseMySQL(
                    host=environment_mysql.host,
                    port=environment_mysql.port,
                    database=environment_mysql.database,
                    user=environment_mysql.user,
                    password=environment_mysql.password,
                ),
            ),
        )

    def authenticate(self, authorization: str):
        self.authenticator.verify(authorization)

    def create_camera_client(self, entity_camera_client: EntityCameraClient):
        self.database_camera_clients.insert(entity_camera_client)
