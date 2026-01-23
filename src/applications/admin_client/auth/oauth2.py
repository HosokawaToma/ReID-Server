from domain.client.auth_credentials import DomainClientAuthCredentials
from domain.client.id import DomainClientId
from environment import Environment
from error import Error
from dto.admin_client.auth.token import DtoAdminClientAuthToken
from dto.admin_client.id import DtoAdminClientId


class ApplicationAdminClientAuthOAuth2Error(Error):
    pass

class ApplicationAdminClientAuthOAuth2InvalidTokenError(ApplicationAdminClientAuthOAuth2Error):
    pass

class ApplicationAdminClientAuthOAuth2:
    def __init__(
        self,
        refresh_secret_key: str,
        refresh_algorithm: str,
        refresh_expire_minutes: int,
    ):
        self.refresh_secret_key = refresh_secret_key
        self.refresh_algorithm = refresh_algorithm
        self.refresh_expire_minutes = refresh_expire_minutes

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationAdminClientAuthOAuth2":
        return cls(
            refresh_secret_key=environment.jwt_refresh_secret_key,
            refresh_algorithm=environment.jwt_refresh_algorithm,
            refresh_expire_minutes=environment.jwt_refresh_expire_minutes,
        )

    def oauth2(self, token: DtoAdminClientAuthToken) -> DtoAdminClientId:
        """
        アドミンクライアントのOAuth2認証を行う
        :param DtoAdminClientAuthToken token: アドミンクライアントのOAuth2認証トークン
        :return DtoAdminClientId: アドミンクライアントのID
        :raises ApplicationAdminClientAuthOAuth2InvalidTokenError: アドミンクライアントのOAuth2認証トークンが不正な場合に発生するエラー
        """
        try:
            id = DomainClientAuthCredentials.convert_token(
                token=token.token,
                secret_key=self.refresh_secret_key,
                algorithm=self.refresh_algorithm,
            )
        except Error as error:
            raise ApplicationAdminClientAuthOAuth2InvalidTokenError(error)
        return DtoAdminClientId(id=str(id))
