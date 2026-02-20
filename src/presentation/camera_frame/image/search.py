"""
カメラフレーム画像検索のプレゼンテーション層

カメラフレームIDを受け取り、画像をストリーミングで返す。
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
    カメラフレーム画像検索のAPIエンドポイントを提供するプレゼンテーションクラス。
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
        カメラフレームIDで画像を取得し、画像レスポンスで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationUtilRequest request: リクエスト
        :param PresentationUtilPathUUID id: カメラフレームID
        :param ApplicationCameraFrameImageSearch application: カメラフレーム画像検索アプリケーション
        :return PresentationUtilImageResponse: 画像ストリーミングレスポンス
        """
        image = application.search(
            id=DtoId(id=id),
        )
        return PresentationUtilImageResponse(status=200, image=image)
