"""
人物検出クエリ検索（ジャンク）のプレゼンテーション層

日付とページでジャンクのクエリID一覧とページングをJSONで返す。
"""
from presentation.utils.base import PresentationUtilBase
from logger import Logger
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.type import PresentationUtilPathDate, PresentationUtilPathInt
from applications.person.snapshot.search import ApplicationPersonSnapshotSearch
from dto.date import DtoDate


class PresentationPersonSnapshotSearchQueryIsJunk(PresentationUtilBase):
    """
    指定日に「ゴミ」とマークされた人物検出のクエリID一覧取得 API を担当するプレゼンテーション。

    パスで日付・ページを受け取り、該当ID一覧とページング情報を JSON で返す。
    """
    router_path = "/person/snapshot/search/query/is_junk/{date}/{page}"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshots query is junk"
    description = "Search person snapshots query is junk"
    responses = {
        200: {
            "description": "Person snapshots query is junk found",
        },
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotSearchQueryIsJunk":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotSearchQueryIsJunk: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_snapshot_search_query_is_junk"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        date: PresentationUtilPathDate,
        page: PresentationUtilPathInt,
        application: ApplicationPersonSnapshotSearch = get_application(
            ApplicationPersonSnapshotSearch),
    ):
        """
        指定日のジャンククエリID一覧とページングを取得し、JSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationUtilPathDate date: 対象日
        :param PresentationUtilPathInt page: ページ番号
        :param ApplicationPersonSnapshotSearch application: 人物検出検索アプリケーション
        :return PresentationUtilJSONResponse: クエリID一覧とページングを含むJSONレスポンス
        """
        ids = application.search_query_is_junk(
            date=DtoDate(year=date.year, month=date.month, day=date.day),
            page=page,
        )
        pagination = application.search_query_is_junk_paging(
            date=DtoDate(year=date.year, month=date.month, day=date.day),
        )
        return PresentationUtilJSONResponse(status=200, content={
            "person_snapshot_query_ids": [
                str(id.id) for id in ids
            ],
            "pagination": {
                "total_items": pagination.total_items,
                "total_pages": pagination.total_pages,
            },
        })
