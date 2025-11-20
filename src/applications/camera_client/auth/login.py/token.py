from entities.camera_client.auth.token import EntityCameraClientAuthToken
from entities.camera_client import EntityCameraClient
from modules.token.verifier import ModuleTokenVerifier
from entities.camera_client.auth.token_embedding import EntityCameraClientAuthTokenEmbedding

class ApplicationCameraClientAuthLoginToken:
    def __init__(self, token_verifier: ModuleTokenVerifier) -> None:
        self.token_verifier = token_verifier

    def login(self, token: EntityCameraClientAuthToken) -> EntityCameraClientAuthTokenEmbedding:
        return EntityCameraClientAuthTokenEmbedding.from_dict(
            self.token_verifier.verify(token.token)
        )
