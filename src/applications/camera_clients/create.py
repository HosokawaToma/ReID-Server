from entities.camera_client import EntityCameraClient
from repositories.database.camera_clients import RepositoryDatabaseCameraClients
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from repositories.database import RepositoryDatabaseEngine
from dataclasses import dataclass
from modules.hasher import ModuleHasher
from environment import EnvironmentHash
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
        environment_postgresql: EntityEnvironmentPostgreSQL,
        environment_hash: EnvironmentHash,
    ) -> "ApplicationCameraClientsCreate":
        return cls(
            database_camera_clients=RepositoryDatabaseCameraClients(
                database=RepositoryDatabaseEngine(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                    database=environment_postgresql.database,
                )
            ),
            hasher=ModuleHasher(secret=environment_hash.secret),
        )

    def create_camera_client(self, params: ApplicationCameraClientsCreateParams) -> None:
        self.database_camera_clients.add(EntityCameraClient(
            id=params.id,
            hashed_password=self.hasher.hash(params.password),
            camera_id=params.camera_id,
            view_id=params.view_id,
        ))
