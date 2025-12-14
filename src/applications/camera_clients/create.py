from entities.camera_client import EntityCameraClient
from repositories.database.camera_clients import RepositoryDatabaseCameraClients
from repositories.database import RepositoryDatabaseEngine
from dataclasses import dataclass
from modules.hasher import ModuleHasher
from environment import Environment
@dataclass
class ApplicationCameraClientsCreateParams:
    id: str
    password: str
    camera_id: int
    view_id: int

class ApplicationCameraClientsCreateError(Exception):
    pass

class ApplicationCameraClientsCreate:
    def __init__(
        self,
        database_camera_clients: RepositoryDatabaseCameraClients,
        hasher: ModuleHasher,
    ):
        self.database_camera_clients = database_camera_clients
        self.hasher = hasher

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ApplicationCameraClientsCreate":
        return cls(
            database_camera_clients=RepositoryDatabaseCameraClients(
                database=RepositoryDatabaseEngine(
                    host=environment.database_host,
                    port=environment.database_port,
                    user=environment.database_user,
                    password=environment.database_password,
                    database=environment.database_database,
                )
            ),
            hasher=ModuleHasher(secret=environment.hash_key),
        )

    def create_camera_client(self, params: ApplicationCameraClientsCreateParams) -> None:
        self.database_camera_clients.add(EntityCameraClient(
            id=params.id,
            hashed_password=self.hasher.hash(params.password),
            camera_id=params.camera_id,
            view_id=params.view_id,
        ))
