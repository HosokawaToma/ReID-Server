"""
人物検出最近傍検索のプレゼンテーション層

人物検出IDとページを受け取り、同日で特徴量が近い順の一覧とページングをJSONで返す。
"""
from presentation.utils.base import PresentationUtilBase
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.type import PresentationUtilPathInt, PresentationUtilPathUUID
from presentation.utils.factory import get_application
from logger import Logger
from applications.person.snapshot.search.nearest import ApplicationPersonSnapshotSearchNearest
from dto.id import DtoId


class PresentationPersonSnapshotSearchNearest(PresentationUtilBase):
    """
    人物検出最近傍検索のAPIエンドポイントを提供するプレゼンテーションクラス。
    """
    router_path = "/person/snapshot/search/nearest/{person_snapshot_id}/{page}"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search nearest person snapshots"
    description = "Search nearest person snapshots"
    responses = {
        200: {
            "description": "Person snapshots found",
        },
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotSearchNearest":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotSearchNearest: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_snapshot_search_nearest"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        person_snapshot_id: PresentationUtilPathUUID,
        page: PresentationUtilPathInt,
        application: ApplicationPersonSnapshotSearchNearest = get_application(
            ApplicationPersonSnapshotSearchNearest),
    ):
        """
        人物検出IDとページで最近傍検索結果を取得し、JSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationUtilPathUUID person_snapshot_id: 人物検出結果ID
        :param PresentationUtilPathInt page: ページ番号
        :param ApplicationPersonSnapshotSearchNearest application: 最近傍検索アプリケーション
        :return PresentationUtilJSONResponse: 最近傍一覧とページングを含むJSONレスポンス
        """
        items = application.search(person_snapshot_id=DtoId(
            id=person_snapshot_id), page=page)
        pagination = application.search_paging(
            person_snapshot_id=DtoId(id=person_snapshot_id))
        return PresentationUtilJSONResponse(status=200, content={
            "person_snapshots": [
                {
                    "id": str(item.id),
                    "camera_id": item.camera_id,
                    "view_id": item.view_id,
                    "timestamp": item.timestamp.isoformat(),
                    "is_junk": item.is_junk,
                    "person_id": str(item.person_id) if item.person_id is not None else None,
                } for item in items
            ],
            "pagination": {
                "total_items": pagination.total_items,
                "total_pages": pagination.total_pages,
            },
        })
