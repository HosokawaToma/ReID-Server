from entities.camera_client import EntityCameraClient
from modules.database.camera_clients import ModuleDatabaseCameraClients
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from database import Database

class ApplicationCameraClientsCreate:
    def __init__(
        self,
        database_camera_clients: ModuleDatabaseCameraClients,
    ):
        self.database_camera_clients = database_camera_clients

    @classmethod
    def create(
        cls,
        environment_postgresql: EntityEnvironmentPostgreSQL,
    ) -> "ApplicationCameraClientsCreate":
        return cls(
            database_camera_clients=ModuleDatabaseCameraClients(
                Database(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    database=environment_postgresql.database,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                ),
            ),
        )

    def create_camera_client(self, entity_camera_client: EntityCameraClient):
        self.database_camera_clients.insert(entity_camera_client)
