from domain.client.auth_credentials import DomainClientAuthCredentials
from domain.client.id import DomainClientId
from domain.client.password import DomainClientPassword
from domain.client.token import DomainClientToken
from domain.token import DomainToken
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
        client_auth_credentials: DomainClientAuthCredentials,
        secret_key: str,
        algorithm: str,
        expire_minutes: int,
        refresh_secret_key: str,
        refresh_algorithm: str,
        refresh_expire_minutes: int,
    ):
        self.client_auth_credentials = client_auth_credentials
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes
        self.refresh_secret_key = refresh_secret_key
        self.refresh_algorithm = refresh_algorithm
        self.refresh_expire_minutes = refresh_expire_minutes

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationAdminClientAuthTokenRefresh":
        return cls(
            client_auth_credentials=DomainClientAuthCredentials(
                id=DomainClientId(id=environment.admin_client_id),
                password=DomainClientPassword(password=environment.admin_client_password),
            ),
            secret_key=environment.jwt_secret_key,
            algorithm=environment.jwt_algorithm,
            expire_minutes=environment.jwt_expire_minutes,
            refresh_secret_key=environment.jwt_refresh_secret_key,
            refresh_algorithm=environment.jwt_refresh_algorithm,
            refresh_expire_minutes=environment.jwt_refresh_expire_minutes,
        )

    def refresh(self, refresh_token: DtoAdminClientAuthToken) -> DtoAdminClientAuthResult:
        """
        アドミンクライアントのトークンを更新する
        :param DtoAdminClientAuthToken refresh_token: アドミンクライアントのトークン更新用トークン
        :return DtoAdminClientAuthResult: アドミンクライアントのトークン更新結果
        :raises ApplicationAdminClientAuthTokenRefreshInvalidRefreshTokenError: アドミンクライアントのトークン更新用トークンが不正な場合に発生するエラー
        """
        try:
            client_token = DomainClientToken.decode(
                token=DomainToken(token=refresh_token.token),
                secret_key=self.refresh_secret_key,
                algorithm=self.refresh_algorithm,
            )
            if client_token.is_expired():
                raise ApplicationAdminClientAuthTokenRefreshInvalidRefreshTokenError()
        except Error as error:
            raise ApplicationAdminClientAuthTokenRefreshInvalidRefreshTokenError(error)
        return DtoAdminClientAuthResult(
            token=self.client_auth_credentials.to_token(
                secret_key=self.secret_key,
                algorithm=self.algorithm,
                expire_minutes=self.expire_minutes,
            ).token,
            refresh_token=self.client_auth_credentials.to_token(
                secret_key=self.refresh_secret_key,
                algorithm=self.refresh_algorithm,
                expire_minutes=self.refresh_expire_minutes,
            ).token,
        )
