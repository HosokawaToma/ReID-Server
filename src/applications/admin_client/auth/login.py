from domain.admin_client import DomainAdminClient
from domain.token_converter import DomainTokenConverter
from environment import Environment
from error import Error
from dataclasses import dataclass

@dataclass
class ApplicationAdminClientAuthLoginParams:
    id: str
    password: str

@dataclass
class ApplicationAdminClientAuthLoginResult:
    token: str
    refresh_token: str

class ApplicationAdminClientAuthLoginError(Error):
    pass

class ApplicationAdminClientAuthLoginInvalidCredentialsError(ApplicationAdminClientAuthLoginError):
    pass

class ApplicationAdminClientAuthLogin:
    def __init__(
        self,
        admin_client: DomainAdminClient,
        token_converter: DomainTokenConverter,
        refresh_token_converter: DomainTokenConverter,
    ):
        self.admin_client = admin_client
        self.token_converter = token_converter
        self.refresh_token_converter = refresh_token_converter

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationAdminClientAuthLogin":
        return cls(
            admin_client=DomainAdminClient(id=environment.admin_client_id, password=environment.admin_client_password),
            token_converter=DomainTokenConverter(
                secret_key=environment.jwt_secret_key,
                algorithm=environment.jwt_algorithm,
                expire_minutes=environment.jwt_expire_minutes,
            ),
            refresh_token_converter=DomainTokenConverter(
                secret_key=environment.jwt_refresh_secret_key,
                algorithm=environment.jwt_refresh_algorithm,
                expire_minutes=environment.jwt_refresh_expire_minutes,
            ),
        )

    def login(self, params: ApplicationAdminClientAuthLoginParams) -> ApplicationAdminClientAuthLoginResult:
        if not self.admin_client.authenticate(params.id, params.password):
            raise ApplicationAdminClientAuthLoginInvalidCredentialsError()
        return ApplicationAdminClientAuthLoginResult(
            token=self.admin_client.generate_token(self.token_converter),
            refresh_token=self.admin_client.generate_token(self.refresh_token_converter),
        )
