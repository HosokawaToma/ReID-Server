"""
人物検出最近傍検索のプレゼンテーション層

POST /person/snapshot/search/nearest/{person_snapshot_id}/{page} で人物検出 ID とページを受け取り、同日の人物検出のうち特徴量が近い順の一覧とページングを JSON で返す API を提供する。認証済み管理クライアントのみ。成功時は 200。
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
    人物検出最近傍検索の API エンドポイントを提供するプレゼンテーションクラス。

    POST /person/snapshot/search/nearest/{person_snapshot_id}/{page} でパスの ID をクエリとし、同日の人物検出のうち特徴量類似度が高い順の一覧をページ単位で取得する。成功時は 200 と person_snapshots, pagination を返す。Bearer トークン必須。
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
        人物検出 ID とページで最近傍検索結果を取得し、JSON で返す。

        パスの person_snapshot_id をクエリ、page でページ指定し、アプリケーション層で search と search_paging を呼ぶ。レスポンスには類似度順の人物検出一覧（id, camera_id, view_id, timestamp, is_junk, person_id）と pagination を含める。クエリに該当する人物検出が無い場合は NotFoundError（404）。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationUtilPathUUID person_snapshot_id: クエリとする人物検出結果 ID（パス）
        :param PresentationUtilPathInt page: ページ番号（パス）
        :param ApplicationPersonSnapshotSearchNearest application: 最近傍検索アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と person_snapshots, pagination
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
