from domain.admin_client import DomainAdminClient
from domain.token_converter import DomainTokenConverter
from environment import Environment
from error import Error
from dataclasses import dataclass

@dataclass
class ApplicationAdminClientAuthTokenRefreshParams:
    refresh_token: str

@dataclass
class ApplicationAdminClientAuthTokenRefreshResult:
    token: str

class ApplicationAdminClientAuthTokenRefreshError(Error):
    pass

class ApplicationAdminClientAuthTokenRefresh:
    def __init__(
        self,
        admin_client: DomainAdminClient,
        token_converter: DomainTokenConverter,
        refresh_token_converter: DomainTokenConverter,
    ):
        self.admin_client = admin_client
        self.token_converter = token_converter
        self.refresh_token_converter = refresh_token_converter

    def refresh(self, params: ApplicationAdminClientAuthTokenRefreshParams) -> ApplicationAdminClientAuthTokenRefreshResult:
        if not self.admin_client.verify_token(params.refresh_token, self.refresh_token_converter):
            raise ApplicationAdminClientAuthTokenRefreshError("Invalid refresh token")
        return ApplicationAdminClientAuthTokenRefreshResult(
            token=self.admin_client.generate_token(self.token_converter),
        )
