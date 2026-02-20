"""
管理認証トークンリフレッシュのプレゼンテーション層

POST /admin/auth/token/refresh で Cookie に含まれるリフレッシュトークンを検証し、
有効な場合は新しいアクセストークンとリフレッシュトークンを発行して 200 で返す。無効・期限切れ時は 401。認証は不要。
"""
from presentation.utils.base import PresentationUtilBase
from presentation.utils.factory import get_application
from logger import Logger
from presentation.utils.request import PresentationUtilRequest
from presentation.utils.response import PresentationUtilJSONResponse
from applications.admin_client.auth.token_refresh import ApplicationAdminClientAuthTokenRefresh
from dto.admin_client.auth.token import DtoAdminClientAuthToken


class PresentationAdminAuthTokenRefresh(PresentationUtilBase):
    """
    管理認証トークンリフレッシュの API エンドポイントを担当するプレゼンテーション。

    POST /admin/auth/token/refresh でリクエストに付与された Cookie の refresh_token を読み、
    有効な場合は新しいアクセストークン（JSON）と新しいリフレッシュトークン（Cookie）を返して 200 とする。無効・期限切れ時は 401。
    """
    router_path = "/admin/auth/token/refresh"
    methods = ["POST"]
    tags = ["Admin Auth"]
    summary = "Refresh admin token"
    description = "Refresh admin token"
    responses = {
        200: {"description": "Token refreshed"},
        401: {"description": "Invalid token"},
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationAdminAuthTokenRefresh":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationAdminAuthTokenRefresh: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_admin_auth_token_refresh"),
        )

    async def handle(
        self,
        request: PresentationUtilRequest,
        application: ApplicationAdminClientAuthTokenRefresh = get_application(
            ApplicationAdminClientAuthTokenRefresh),
    ):
        """
        Cookie のリフレッシュトークンでトークンを更新し、新しいアクセス・リフレッシュトークンを返す。

        リクエストの Cookie から refresh_token を取得し、アプリケーション層で検証・新トークン発行を行う。
        成功時は 200 と JSON（token）、および Set-Cookie で新しい refresh_token を返す。無効・期限切れ時は AuthenticationError により 401。

        :param PresentationUtilRequest request: リクエスト（request.cookies から refresh_token を参照）
        :param ApplicationAdminClientAuthTokenRefresh application: トークンリフレッシュを行うアプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 時は {"token": "..."}、Cookie に refresh_token を設定
        :raises AuthenticationError: リフレッシュトークンが不正または期限切れの場合（HTTP 401）
        """
        result = application.refresh(
            DtoAdminClientAuthToken(
                token=request.cookies.get("refresh_token", ""),
            ),
        )
        response = PresentationUtilJSONResponse(
            status=200, content={"token": result.token})
        response.set_refresh_token(refresh_token=result.refresh_token)
        return response
