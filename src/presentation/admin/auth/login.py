"""
管理認証ログインのプレゼンテーション層

管理クライアントのログイン API を提供する。POST で ID とパスワードを受け取り、認証成功時はアクセストークンを JSON、
リフレッシュトークンを Cookie に設定して 200 を返す。認証失敗時は 401 を返す。認証は不要。
"""
from presentation.utils.base import PresentationUtilBase
from presentation.utils.factory import get_application
from logger import Logger
from presentation.utils.request import PresentationUtilRequest
from presentation.utils.request import PresentationUtilRequestBody
from presentation.utils.response import PresentationUtilJSONResponse
from applications.admin_client.auth.login import ApplicationAdminClientAuthLogin
from dto.admin_client.auth.credentials import DtoAdminClientAuthCredentials


class PresentationAdminAuthLoginRequestBody(PresentationUtilRequestBody):
    """
    管理認証ログイン API のリクエストボディを保持する DTO。

    管理クライアントを識別する ID（文字列）とパスワードを必須で保持する。POST ボディで送信する。
    """
    id: str
    password: str


class PresentationAdminAuthLogin(PresentationUtilBase):
    """
    管理認証ログインの API エンドポイントを担当するプレゼンテーション。

    POST /admin/auth/login でリクエストボディの ID・パスワードを検証し、成功時は 200 とともに
    アクセストークンを JSON に、リフレッシュトークンを Cookie（refresh_token）に設定して返す。
    資格情報が不正または期限切れの場合は 401 を返す。
    """
    router_path = "/admin/auth/login"
    methods = ["POST"]
    tags = ["Admin Auth"]
    summary = "Login admin"
    description = "Login admin"
    responses = {
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials"},
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationAdminAuthLogin":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationAdminAuthLogin: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_admin_auth_login"),
        )

    async def handle(
        self,
        request: PresentationUtilRequest,
        body: PresentationAdminAuthLoginRequestBody,
        application: ApplicationAdminClientAuthLogin = get_application(
            ApplicationAdminClientAuthLogin),
    ):
        """
        リクエストボディの ID・パスワードでログインし、成功時はトークンを返す。

        アプリケーション層で資格情報を検証し、有効な場合はアクセストークンとリフレッシュトークンを生成する。
        レスポンスにはアクセストークンを JSON に含め、リフレッシュトークンは Set-Cookie で送る。不正時は AuthenticationError により 401 となる。

        :param PresentationUtilRequest request: FastAPI のリクエスト（本処理では未使用だが Depends の都合で受け取る）
        :param PresentationAdminAuthLoginRequestBody body: 管理クライアント ID とパスワード
        :param ApplicationAdminClientAuthLogin application: ログイン処理を行うアプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 時は {"token": "..."}、Cookie に refresh_token を設定
        :raises AuthenticationError: 資格情報が不正な場合（HTTP 401）
        """
        result = application.login(
            DtoAdminClientAuthCredentials(
                id=body.id,
                password=body.password,
            ),
        )
        response = PresentationUtilJSONResponse(
            status=200, content={"token": result.token})
        response.set_refresh_token(refresh_token=result.refresh_token)
        return response
