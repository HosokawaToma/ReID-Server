from entities.admin_client.auth.token import EntityAdminClientAuthToken
from modules.token.verifier import ModuleTokenVerifier
from entities.admin_client.auth.token_embedding import EntityAdminClientAuthTokenEmbedding

class ApplicationAdminClientAuthLoginToken:
    def __init__(self, verifier: ModuleTokenVerifier) -> None:
        self.verifier = verifier

    def login(self, token: EntityAdminClientAuthToken) -> EntityAdminClientAuthTokenEmbedding:
        return EntityAdminClientAuthTokenEmbedding.from_dict(
            self.verifier.verify(token.token)
        )
