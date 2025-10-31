from entities.camera_client import EntityCameraClient
from modules.database.mysql.camera_clients import ModuleDatabaseMySQLCameraClients
from modules.authenticator.camera_client import ModuleAuthenticatorCameraClient
from database.mysql import DatabaseMySQL
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.mysql import EntityEnvironmentMysql

class ApplicationLoginCameraClient:
    def __init__(
        self,
        database_camera_clients: ModuleDatabaseMySQLCameraClients,
        authenticator_camera_client: ModuleAuthenticatorCameraClient,
        ):
        self.database_camera_clients = database_camera_clients
        self.authenticator_camera_client = authenticator_camera_client

    @classmethod
    def create(
        cls,
        environment_jwt: EntityEnvironmentJwt,
        environment_mysql: EntityEnvironmentMysql,
    ) -> "ApplicationLoginCameraClient":
        return cls(
            database_camera_clients=ModuleDatabaseMySQLCameraClients(DatabaseMySQL(
                host=environment_mysql.host,
                port=environment_mysql.port,
                user=environment_mysql.user,
                password=environment_mysql.password,
                database=environment_mysql.database,
            )),
            authenticator_camera_client=ModuleAuthenticatorCameraClient(
                jwt_secret_key=environment_jwt.secret_key,
                jwt_algorithm=environment_jwt.algorithm,
            ),
        )

    def login(self, camera_client_id: str, password: str):
        camera_client = EntityCameraClient(camera_client_id, password)
        database_camera_client = self.database_camera_clients.select_by_id(camera_client.id)
        if database_camera_client.hashed_password != camera_client.hashed_password:
            raise Exception("Invalid camera_client_id or password")
        return self.authenticator_camera_client.generate_token(camera_client)
