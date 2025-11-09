from modules.auth.verify.camera_client import ModuleAuthVerifyCameraClient
from modules.auth.generate_token.camera_client import ModuleAuthGenerateTokenCameraClient
from entities.jwt.camera_client import EntityJWTCameraClient
from entities.camera_client import EntityCameraClient
from modules.database.camera_clients import ModuleDatabaseCameraClients
from entities.environment.jwt import EntityEnvironmentJwt
from database import Database
from entities.environment.postgresql import EntityEnvironmentPostgreSQL

class ApplicationAuthCameraClient:
    def __init__(
        self,
        database_camera_clients: ModuleDatabaseCameraClients,
        verifier: ModuleAuthVerifyCameraClient,
        generator: ModuleAuthGenerateTokenCameraClient,
    ):
        self.database_camera_clients = database_camera_clients
        self.verifier = verifier
        self.generator = generator

    def login(self, id: str, password: str) -> EntityCameraClient:
        camera_client = self.database_camera_clients.select_by_id(id)
        request_camera_client = EntityCameraClient(
            id=id,
            password=password,
            camera_id=camera_client.camera_id,
            view_id=camera_client.view_id,
            hashed_password=None
        )
        if request_camera_client.hashed_password != camera_client.hashed_password:
            raise Exception("Invalid id or password")
        return request_camera_client

    def verify(self, authorization: str) -> EntityJWTCameraClient:
        return self.verifier(authorization)

    def generate(self, id: str, camera_id: int, view_id: int) -> str:
        return self.generator(id, camera_id, view_id)

    @classmethod
    def create(
        cls,
        environment_postgresql: EntityEnvironmentPostgreSQL,
        environment_jwt: EntityEnvironmentJwt,
    ) -> "ApplicationAuthCameraClient":
        return cls(
            database_camera_clients=ModuleDatabaseCameraClients(
                database=Database(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    database=environment_postgresql.database,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                ),
            ),
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
