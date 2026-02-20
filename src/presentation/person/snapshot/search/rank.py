"""
人物検出ランキング検索のプレゼンテーション層

人物検出IDとページを受け取り、ランキング一覧とページングをJSONで返す。
"""
from presentation.utils.base import PresentationUtilBase
from dto.id import DtoId
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.type import PresentationUtilPathInt, PresentationUtilPathUUID
from logger import Logger
from applications.person.snapshot.search.rank import ApplicationPersonSnapshotSearchRank


class PresentationPersonSnapshotSearchRank(PresentationUtilBase):
    """
    人物検出ランキング検索のAPIエンドポイントを提供するプレゼンテーションクラス。
    """
    router_path = "/person/snapshot/search/rank/{person_snapshot_id}/{page}"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshot rank"
    description = "Search person snapshots with similar features from different cameras on the same date"
    responses = {
        200: {
            "description": "Person snapshot rank found",
        },
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotSearchRank":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotSearchRank: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_snapshot_search_rank"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        person_snapshot_id: PresentationUtilPathUUID,
        page: PresentationUtilPathInt,
        application: ApplicationPersonSnapshotSearchRank = get_application(
            ApplicationPersonSnapshotSearchRank),
    ):
        """
        人物検出IDとページでランキングを取得し、JSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationUtilPathUUID person_snapshot_id: 人物検出結果ID
        :param PresentationUtilPathInt page: ページ番号
        :param ApplicationPersonSnapshotSearchRank application: ランキング検索アプリケーション
        :return PresentationUtilJSONResponse: ランキング一覧とページングを含むJSONレスポンス
        """
        items = application.search(
            person_snapshot_id=DtoId(id=person_snapshot_id),
            page=page,
        )
        paging = application.search_paging(
            person_snapshot_id=DtoId(id=person_snapshot_id))
        return PresentationUtilJSONResponse(status=200, content={
            "person_snapshots": [
                {
                    "id": str(item.id),
                    "camera_id": item.camera_id,
                    "view_id": item.view_id,
                    "timestamp": item.timestamp.isoformat(),
                    "person_id": str(item.person_id) if item.person_id is not None else None,
                    "is_junk": item.is_junk,
                } for item in items
            ],
            "pagination": {
                "total_items": paging.total_items,
                "total_pages": paging.total_pages,
            },
        })
