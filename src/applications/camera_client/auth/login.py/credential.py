from entities.camera_client.auth.credential import EntityCameraClientAuthLoginCredential
from entities.camera_client.auth.token import EntityCameraClientAuthToken
from entities.camera_client.auth.token_embedding import EntityCameraClientAuthTokenEmbedding
from modules.database.camera_clients import ModuleDatabaseCameraClients
from modules.hasher import ModuleHasher
from modules.token.generator import ModuleTokenGenerator

class ApplicationCameraClientAuthLoginCredential:
    TOKEN_PAYLOAD_KEY = "id"
    TOKEN_PAYLOAD_KEY_CAMERA_ID = "camera_id"
    TOKEN_PAYLOAD_KEY_VIEW_ID = "view_id"

    def __init__(
        self,
        database: ModuleDatabaseCameraClients,
        hasher: ModuleHasher,
        token_generator: ModuleTokenGenerator
    ) -> None:
        self.database = database
        self.hasher = hasher
        self.token_generator = token_generator

    def login(self, params: EntityCameraClientAuthLoginCredential) -> EntityCameraClientAuthToken:
        camera_client = self.database.select_by_id(params.id)
        self.hasher.assert_valid(params.password, camera_client.hashed_password)
        return EntityCameraClientAuthToken(
            self.token_generator.generate(
                EntityCameraClientAuthTokenEmbedding(
                    id=camera_client.id,
                    camera_id=camera_client.camera_id,
                    view_id=camera_client.view_id,
                ).to_dict()
            )
        )
