"""
管理クライアント OAuth2 認証アプリケーション

Bearer トークンを検証し、管理クライアントIDを返す。
"""
from domain.client.token import DomainClientToken
from domain.token import DomainToken
from environment import Environment
from dto.admin_client.auth.token import DtoAdminClientAuthToken
from dto.admin_client.id import DtoAdminClientId
from error import AuthenticationError


class ApplicationAdminClientAuthOAuth2:
    """
    Bearer トークンによる管理クライアント認証を行うアプリケーションクラス。
    """

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        expire_minutes: int,
    ):
        """
        アプリケーションを初期化する。

        :param str secret_key: JWT署名鍵
        :param str algorithm: JWTアルゴリズム
        :param int expire_minutes: トークン有効分数
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationAdminClientAuthOAuth2":
        """
        環境からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return ApplicationAdminClientAuthOAuth2: アプリケーションインスタンス
        """
        return cls(
            secret_key=environment.jwt_secret_key,
            algorithm=environment.jwt_algorithm,
            expire_minutes=environment.jwt_expire_minutes,
        )

    def oauth2(self, token: DtoAdminClientAuthToken) -> DtoAdminClientId:
        """
        アドミンクライアントのOAuth2認証を行う
        :param DtoAdminClientAuthToken token: アドミンクライアントのOAuth2認証トークン
        :return DtoAdminClientId: アドミンクライアントのID
        :raises ApplicationAdminClientAuthOAuth2InvalidTokenError: アドミンクライアントのOAuth2認証トークンが不正な場合に発生するエラー
        """
        client_token = DomainClientToken.decode(
            token=DomainToken(token=token.token),
            secret_key=self.secret_key,
            algorithm=self.algorithm,
        )
        if client_token.is_expired():
            raise AuthenticationError("アドミンクライアントのOAuth2認証トークンが期限切れです")
        return DtoAdminClientId(id=str(client_token.client_id))
