"""
人物検出ギャラリー検索（ジャンク含む）のプレゼンテーション層

POST /person/snapshot/search/gallery/contains_junk/{person_snapshot_id} で人物検出 ID をクエリとし、同日・別カメラの類似度順ギャラリー ID 一覧（ゴミ含む）を JSON で返す API を提供する。評価用。認証済み管理クライアントのみ。成功時は 200。
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
    人物検出をクエリとしたギャラリー（正解含む・類似度順 ID 一覧）取得 API を担当するプレゼンテーション。

    POST /person/snapshot/search/gallery/contains_junk/{person_snapshot_id} でパスの ID をクエリとし、同日の別カメラで類似度順に並べた人物検出 ID 一覧（ゴミ含む）を取得する。正解がギャラリーに含まれることを前提とした評価用。成功時は 200 と person_snapshot_gallery_ids を返す。Bearer トークン必須。
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
        指定した人物検出をクエリに、正解含むギャラリー ID 一覧（類似度順・ゴミ含む）を取得し、JSON で返す。

        パスの person_snapshot_id をクエリとし、アプリケーション層で同日・別カメラの類似度順 ID 一覧を取得する。正解が無い場合は ValidationError により 400 となる。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationUtilPathUUID person_snapshot_id: クエリとする人物検出結果 ID（パス）
        :param ApplicationPersonSnapshotSearch application: 人物検出検索アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と {"person_snapshot_gallery_ids": [...]}
        """
        ids = application.search_gallery_contains_junk(
            person_snapshot_id=DtoId(id=person_snapshot_id))
        return PresentationUtilJSONResponse(status=200, content={
            "person_snapshot_gallery_ids": [str(id.id) for id in ids],
        })
