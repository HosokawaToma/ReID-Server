"""
人物検出画像検索のプレゼンテーション層

人物検出IDを受け取り、画像をストリーミングで返す。
"""
from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearch
from dto.id import DtoId
from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.request import PresentationUtilRequest
from presentation.utils.response import PresentationUtilImageResponse
from presentation.utils.type import PresentationUtilPathUUID
from logger import Logger


class PresentationPersonSnapshotImageSearch(PresentationUtilBase):
    """
    人物検出画像検索のAPIエンドポイントを提供するプレゼンテーションクラス。
    """
    router_path = "/person/snapshot/image/search/{id}"
    methods = ["GET"]
    tags = ["Person Snapshot Image"]
    summary = "Search person snapshot image"
    description = "Search person snapshot image by image id"
    responses = {
        200: {
            "description": "Person snapshot image found",
        },
        404: {
            "description": "Person snapshot image not found",
        },
        500: {
            "description": "Internal server error",
        },
    }

    def __init__(
        self,
        logger: Logger,
    ):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotImageSearch":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotImageSearch: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_snapshot_image_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationUtilRequest,
        id: PresentationUtilPathUUID,
        application: ApplicationPersonSnapshotImageSearch = get_application(
            ApplicationPersonSnapshotImageSearch),
    ):
        """
        人物検出IDで画像を取得し、画像レスポンスで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationUtilRequest request: リクエスト
        :param PresentationUtilPathUUID id: 人物検出結果ID
        :param ApplicationPersonSnapshotImageSearch application: 人物検出画像検索アプリケーション
        :return PresentationUtilImageResponse: 画像ストリーミングレスポンス
        """
        image = application.search(
            id=DtoId(id=id),
        )
        return PresentationUtilImageResponse(status=200, image=image)
