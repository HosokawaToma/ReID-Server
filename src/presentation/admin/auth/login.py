"""
管理認証ログインのプレゼンテーション層

ID・パスワードを受け取り、トークンとリフレッシュトークンをJSONとCookieで返す。
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
    """管理認証ログインAPIのリクエストボディ。"""
    id: str
    password: str


class PresentationAdminAuthLogin(PresentationUtilBase):
    """
    管理認証ログインのAPIエンドポイントを提供するプレゼンテーションクラス。
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
        認証情報でログインし、トークンをJSON、リフレッシュトークンをCookieで返す。

        :param PresentationUtilRequest request: リクエスト
        :param PresentationAdminAuthLoginRequestBody body: ID・パスワード
        :param ApplicationAdminClientAuthLogin application: ログインアプリケーション
        :return PresentationUtilJSONResponse: トークンを含むJSONレスポンス（Cookieにリフレッシュトークン設定）
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
