from entities.camera_client import EntityCameraClient
from modules.database.camera_clients import ModuleDatabaseCameraClients
from modules.authenticator.camera_client import ModuleAuthenticatorCameraClient
from database import Database
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.postgresql import EntityEnvironmentPostgreSQL

class ApplicationLoginCameraClient:
    def __init__(
        self,
        database_camera_clients: ModuleDatabaseCameraClients,
        authenticator_camera_client: ModuleAuthenticatorCameraClient,
        ):
        self.database_camera_clients = database_camera_clients
        self.authenticator_camera_client = authenticator_camera_client

    @classmethod
    def create(
        cls,
        environment_jwt: EntityEnvironmentJwt,
        environment_postgresql: EntityEnvironmentPostgreSQL,
    ) -> "ApplicationLoginCameraClient":
        return cls(
            database_camera_clients=ModuleDatabaseCameraClients(Database(
                host=environment_postgresql.host,
                port=environment_postgresql.port,
                user=environment_postgresql.user,
                password=environment_postgresql.password,
                database=environment_postgresql.database,
            )),
            authenticator_camera_client=ModuleAuthenticatorCameraClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_days=environment_jwt.expire_days,
            ),
        )

    def login(self, camera_client_id: str, password: str):
        database_camera_client = self.database_camera_clients.select_by_id(camera_client_id)
        camera_client = EntityCameraClient(
            id=database_camera_client.id,
            password=password,
            hashed_password=None,
            camera_id=database_camera_client.camera_id,
            view_id=database_camera_client.view_id,
        )
        if database_camera_client.hashed_password != camera_client.hashed_password:
            raise Exception("Invalid camera_client_id or password")
        return self.authenticator_camera_client.generate_token(camera_client)
