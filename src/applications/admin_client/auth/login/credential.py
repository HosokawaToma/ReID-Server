from entities.admin_client.auth.credential import EntityAdminClientCredential
from errors.application.admin_client.auth.login.credential import ErrorApplicationAdminClientAuthLoginCredential
from entities.admin_client.auth.token import EntityAdminClientAuthToken
from entities.admin_client.auth.token_embedding import EntityAdminClientAuthTokenEmbedding
from modules.token.generator import ModuleTokenGenerator

class ApplicationAdminClientAuthLoginCredential:
    def __init__(
        self,
        credential: EntityAdminClientCredential,
        token_generator: ModuleTokenGenerator
    ) -> None:
        self.credential = credential
        self.token_generator = token_generator

    def login(self, params: EntityAdminClientCredential) -> EntityAdminClientAuthToken:
        if self.credential.id != params.id or self.credential.password != params.password:
            raise ErrorApplicationAdminClientAuthLoginCredential
        return EntityAdminClientAuthToken(
            self.token_generator.generate(
                EntityAdminClientAuthTokenEmbedding(
                    id=self.credential.id,
                ).to_dict()
            )
        )
