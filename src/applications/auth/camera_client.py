from modules.auth.verify.camera_client import ModuleAuthVerifyCameraClient
from modules.auth.parse_bearer import ModuleAuthParseBearer
from modules.auth.generate_token.camera_client import ModuleAuthGenerateTokenCameraClient
from entities.jwt.camera_client import EntityJWTCameraClient
from entities.camera_client import EntityCameraClient
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from environment import EnvironmentHash
from repositories.database import RepositoryDatabaseEngine
from repositories.database.camera_clients import RepositoryDatabaseCameraClients
from repositories.database.camera_clients import RepositoryDatabaseCameraClientsFilters
from modules.hasher import ModuleHasher
from dataclasses import dataclass

@dataclass
class ApplicationAuthLoginCameraClientParams:
    id: str
    password: str

class ApplicationAuthCameraClient:
    def __init__(
        self,
        database_camera_clients: RepositoryDatabaseCameraClients,
        hasher: ModuleHasher,
        parser: ModuleAuthParseBearer,
        verifier: ModuleAuthVerifyCameraClient,
        generator: ModuleAuthGenerateTokenCameraClient,
    ):
        self.database_camera_clients = database_camera_clients
        self.hasher = hasher
        self.parser = parser
        self.verifier = verifier
        self.generator = generator

    def login(self, params: ApplicationAuthLoginCameraClientParams) -> EntityCameraClient:
        camera_client = self.database_camera_clients.find_first(filters=RepositoryDatabaseCameraClientsFilters(id=params.id))
        self.hasher.matches(params.password, camera_client.hashed_password)
        return camera_client

    def parse(self, authorization: str) -> str:
        return self.parser(authorization)

    def verify(self, token: str) -> EntityJWTCameraClient:
        return self.verifier(token)

    def generate(self, id: str, camera_id: int, view_id: int) -> str:
        return self.generator(id, camera_id, view_id)

    @classmethod
    def create(
        cls,
        environment_postgresql: EntityEnvironmentPostgreSQL,
        environment_jwt: EntityEnvironmentJwt,
        environment_hash: EnvironmentHash,
    ) -> "ApplicationAuthCameraClient":
        return cls(
            database_camera_clients=RepositoryDatabaseCameraClients(
                database=RepositoryDatabaseEngine(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    database=environment_postgresql.database,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                )
            ),
            hasher=ModuleHasher(secret=environment_hash.secret),
            parser=ModuleAuthParseBearer(),
            verifier=ModuleAuthVerifyCameraClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_minutes=environment_jwt.expire_minutes,
            ),
            generator=ModuleAuthGenerateTokenCameraClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_minutes=environment_jwt.expire_minutes,
            ),
        )
