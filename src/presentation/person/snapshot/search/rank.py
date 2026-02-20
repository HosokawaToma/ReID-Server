"""
人物検出ランキング検索のプレゼンテーション層

POST /person/snapshot/search/rank/{person_snapshot_id}/{page} で人物検出 ID とページを受け取り、同日・別カメラで類似度順に並べたランキング一覧とページングを JSON で返す API を提供する。認証済み管理クライアントのみ。成功時は 200。
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
    人物検出ランキング検索の API エンドポイントを提供するプレゼンテーションクラス。

    POST /person/snapshot/search/rank/{person_snapshot_id}/{page} でパスの ID をクエリとし、同日・別カメラの人物検出を特徴量類似度順に並べたランキングをページ単位で取得する。成功時は 200 と person_snapshots, pagination を返す。Bearer トークン必須。
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
        人物検出 ID とページでランキングを取得し、JSON で返す。

        パスの person_snapshot_id をクエリ、page でページ指定し、アプリケーション層で search と search_paging を呼ぶ。レスポンスには同日・別カメラで類似度順に並べた人物検出一覧と pagination を含める。クエリに該当する人物検出が無い場合は NotFoundError（404）。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationUtilPathUUID person_snapshot_id: クエリとする人物検出結果 ID（パス）
        :param PresentationUtilPathInt page: ページ番号（パス）
        :param ApplicationPersonSnapshotSearchRank application: ランキング検索アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と person_snapshots, pagination
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
