"""
カメラフレーム画像検索のプレゼンテーション層

GET /camera_frame/image/search/{id} でカメラフレーム ID を受け取り、ストレージから画像を取得して画像レスポンスで返す API を提供する。
認証済み管理クライアントのみ利用可能。存在しない ID は 404、同一 ID で複数拡張子がある場合は 409、取得失敗時は 500。
"""
from applications.camera_frame.image.search import ApplicationCameraFrameImageSearch
from presentation.utils.base import PresentationUtilBase
from presentation.utils.factory import get_application
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.response import PresentationUtilImageResponse
from presentation.utils.request import PresentationUtilRequest
from presentation.utils.type import PresentationUtilPathUUID
from logger import Logger
from dto.id import DtoId


class PresentationCameraFrameImageSearch(PresentationUtilBase):
    """
    カメラフレーム画像検索の API エンドポイントを提供するプレゼンテーションクラス。

    GET /camera_frame/image/search/{id} でパスの ID に紐づくカメラフレーム画像をストレージから取得し、画像バイナリで返す。成功時は 200 と Content-Type 付きで画像を返す。Bearer トークン必須。
    """
    router_path = "/camera_frame/image/search/{id}"
    methods = ["GET"]
    tags = ["Camera Frame Image"]
    summary = "Search camera frame images"
    description = "Search camera frame images"
    responses = {
        200: {
            "description": "Camera frame images",
        },
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationCameraFrameImageSearch":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationCameraFrameImageSearch: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_camera_frame_image_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationUtilRequest,
        id: PresentationUtilPathUUID,
        application: ApplicationCameraFrameImageSearch = get_application(
            ApplicationCameraFrameImageSearch),
    ) -> PresentationUtilImageResponse:
        """
        カメラフレーム ID で画像を取得し、画像レスポンスで返す。

        パスの ID を DTO に渡し、アプリケーション層でストレージから画像を取得する。取得した画像をそのままレスポンスボディに載せて 200 で返す。画像が無い場合は NotFoundError（404）、同一 ID で複数拡張子が存在する場合は ConflictError（409）。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationUtilRequest request: リクエスト（本処理では未使用）
        :param PresentationUtilPathUUID id: カメラフレーム ID（パス: /camera_frame/image/search/{id}）
        :param ApplicationCameraFrameImageSearch application: カメラフレーム画像検索アプリケーション（Depends で注入）
        :return PresentationUtilImageResponse: 200 と画像バイナリ（Content-Type は画像形式に応じる）
        """
        image = application.search(
            id=DtoId(id=id),
        )
        return PresentationUtilImageResponse(status=200, image=image)
