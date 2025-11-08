from modules.authenticator.admin_client import ModuleAuthenticatorAdminClient
from entities.camera_client import EntityCameraClient
from modules.database.postgresql.camera_clients import ModuleDatabasePostgreSQLCameraClients
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from database.postgresql import DatabasePostgreSQL

class ApplicationCameraClientsCreate:
    def __init__(
        self,
        authenticator: ModuleAuthenticatorAdminClient,
        database_camera_clients: ModuleDatabasePostgreSQLCameraClients,
    ):
        self.authenticator = authenticator
        self.database_camera_clients = database_camera_clients

    @classmethod
    def create(
        cls,
        environment_jwt: EntityEnvironmentJwt,
        environment_postgresql: EntityEnvironmentPostgreSQL,
    ) -> "ApplicationCameraClientsCreate":
        return cls(
            authenticator=ModuleAuthenticatorAdminClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_days=environment_jwt.expire_days,
            ),
            database_camera_clients=ModuleDatabasePostgreSQLCameraClients(
                DatabasePostgreSQL(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    database=environment_postgresql.database,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                ),
            ),
        )

    def authenticate(self, authorization: str):
        self.authenticator.verify(authorization)

    def create_camera_client(self, entity_camera_client: EntityCameraClient):
        self.database_camera_clients.insert(entity_camera_client)
