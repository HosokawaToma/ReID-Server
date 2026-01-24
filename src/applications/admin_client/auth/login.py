from domain.client.auth_credentials import DomainClientAuthCredentials
from domain.client.id import DomainClientId
from domain.client.password import DomainClientPassword
from environment import Environment
from error import Error
from applications import ApplicationBase
from dto.admin_client.auth.credentials import DtoAdminClientAuthCredentials
from dto.admin_client.auth.result import DtoAdminClientAuthResult

class ApplicationAdminClientAuthLoginError(Error):
    pass

class ApplicationAdminClientAuthLoginInvalidCredentialsError(ApplicationAdminClientAuthLoginError):
    pass

class ApplicationAdminClientAuthLogin(ApplicationBase):
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
    def create(cls, environment: Environment) -> "ApplicationAdminClientAuthLogin":
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

    def login(self, credentials: DtoAdminClientAuthCredentials) -> DtoAdminClientAuthResult:
        """
        アドミンクライアントのパスワード認証を行う
        :param DtoAdminClientAuthCredentials credentials: アドミンクライアントのパスワード認証資格情報
        :return DtoAdminClientAuthResult: アドミンクライアントのパスワード認証結果
        :raises ApplicationAdminClientAuthLoginInvalidCredentialsError: アドミンクライアントのパスワード認証資格情報が不正な場合に発生するエラー
        """
        if not self.client_auth_credentials.authenticate(
            id=DomainClientId(id=credentials.id),
            password=DomainClientPassword(password=credentials.password),
        ):
            raise ApplicationAdminClientAuthLoginInvalidCredentialsError()
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
