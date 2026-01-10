from domain.admin_client import DomainAdminClient
from domain.token_converter import DomainTokenConverter
from environment import Environment
from error import Error
from applications import ApplicationBase
from dto.admin_client.auth.token import DtoAdminClientAuthToken
from dto.admin_client.auth.result import DtoAdminClientAuthResult

class ApplicationAdminClientAuthTokenRefreshError(Error):
    pass

class ApplicationAdminClientAuthTokenRefreshInvalidRefreshTokenError(ApplicationAdminClientAuthTokenRefreshError):
    pass

class ApplicationAdminClientAuthTokenRefresh(ApplicationBase):
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
    def create(cls, environment: Environment) -> "ApplicationAdminClientAuthTokenRefresh":
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

    def refresh(self, refresh_token: DtoAdminClientAuthToken) -> DtoAdminClientAuthResult:
        if not self.admin_client.verify_token(refresh_token.token, self.refresh_token_converter):
            raise ApplicationAdminClientAuthTokenRefreshInvalidRefreshTokenError()
        return DtoAdminClientAuthResult(
            token=self.admin_client.generate_token(self.token_converter),
            refresh_token=self.admin_client.generate_token(self.refresh_token_converter),
        )
