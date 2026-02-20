"""
人物検出ギャラリー検索（ジャンク含む）のプレゼンテーション層

人物検出IDを受け取り、同日・別カメラの類似度順ギャラリーID一覧（ジャンク含む）をJSONで返す。
"""
from presentation.utils.base import PresentationUtilBase
from logger import Logger
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.type import PresentationUtilPathUUID
from applications.person.snapshot.search import ApplicationPersonSnapshotSearch
from dto.id import DtoId


class PresentationPersonSnapshotSearchGalleryContainsJunk(PresentationUtilBase):
    """
    人物検出をクエリとしたギャラリー（正解含む類似ID一覧）取得 API を担当するプレゼンテーション。

    パスで人物検出IDを受け取り、正解データを含むギャラリーID一覧を JSON で返す。
    """
    router_path = "/person/snapshot/search/gallery/contains_junk/{person_snapshot_id}"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshots gallery contains junk"
    description = "Search person snapshots gallery contains junk"
    responses = {
        200: {
            "description": "Person snapshots gallery contains junk found",
        },
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotSearchGalleryContainsJunk":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotSearchGalleryContainsJunk: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger(
                "presentation_person_snapshot_search_gallery_contains_junk"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        person_snapshot_id: PresentationUtilPathUUID,
        application: ApplicationPersonSnapshotSearch = get_application(
            ApplicationPersonSnapshotSearch),
    ):
        """
        指定した人物検出をクエリに、ギャラリーID一覧（ジャンク含む）を取得し、JSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationUtilPathUUID person_snapshot_id: 人物検出結果ID（クエリ）
        :param ApplicationPersonSnapshotSearch application: 人物検出検索アプリケーション
        :return PresentationUtilJSONResponse: ギャラリーID一覧を含むJSONレスポンス
        """
        ids = application.search_gallery_contains_junk(
            person_snapshot_id=DtoId(id=person_snapshot_id))
        return PresentationUtilJSONResponse(status=200, content={
            "person_snapshot_gallery_ids": [str(id.id) for id in ids],
        })
