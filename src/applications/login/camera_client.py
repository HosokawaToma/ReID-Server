from entities.camera_client import EntityCameraClient
from modules.database.mysql.camera_clients import ModuleDatabaseMySQLCameraClients
from modules.authenticator.camera_client import ModuleAuthenticatorCameraClient
from database.mysql import DatabaseMySQL

class ApplicationLoginCameraClient:
    def __init__(
        self,
        database_camera_clients: ModuleDatabaseMySQLCameraClients,
        authenticator_camera_client: ModuleAuthenticatorCameraClient,
        ):
        self.database_camera_clients = database_camera_clients
        self.authenticator_camera_client = authenticator_camera_client

    @classmethod
    def create(cls, jwt_secret_key: str, jwt_algorithm: str, mysql_engine_url: str) -> "ApplicationLoginCameraClient":
        return cls(
            database_camera_clients=ModuleDatabaseMySQLCameraClients(DatabaseMySQL(engine_url=mysql_engine_url)),
            authenticator_camera_client=ModuleAuthenticatorCameraClient(jwt_secret_key=jwt_secret_key, jwt_algorithm=jwt_algorithm)
        )

    def login(self, camera_client_id: str, password: str):
        camera_client = EntityCameraClient(camera_client_id, password)
        database_camera_client = self.database_camera_clients.select_by_id(camera_client.id)
        if database_camera_client.hashed_password != camera_client.hashed_password:
            raise Exception("Invalid camera_client_id or password")
        return self.authenticator_camera_client.generate_token(camera_client)
