from domain.admin_client import DomainAdminClient
from domain.token_converter import DomainTokenConverter
from environment import Environment
from error import Error
from dataclasses import dataclass

@dataclass
class ApplicationAdminClientAuthOAuth2Params:
    code: str

@dataclass
class ApplicationAdminClientAuthOAuth2Result:
    id: str

class ApplicationAdminClientAuthOAuth2Error(Error):
    pass

class ApplicationAdminClientAuthOAuth2:
    def __init__(self, admin_client: DomainAdminClient, token_converter: DomainTokenConverter):
        self.admin_client = admin_client
        self.token_converter = token_converter

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationAdminClientAuthOAuth2":
        return cls(
            admin_client=DomainAdminClient(id=environment.admin_client_id, password=environment.admin_client_password),
            token_converter=DomainTokenConverter(
                secret_key=environment.jwt_secret_key,
                algorithm=environment.jwt_algorithm,
                expire_minutes=environment.jwt_expire_minutes,
            ),
        )

    def oauth2(self, params: ApplicationAdminClientAuthOAuth2Params) -> ApplicationAdminClientAuthOAuth2Result:
        id = self.admin_client.verify_token(params.code, self.token_converter)
        if id is None:
            raise ApplicationAdminClientAuthOAuth2Error("Invalid code")
        return ApplicationAdminClientAuthOAuth2Result(
            id=id,
        )
