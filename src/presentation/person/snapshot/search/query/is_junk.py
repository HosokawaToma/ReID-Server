"""
人物検出クエリ検索（ジャンク）のプレゼンテーション層

POST /person/snapshot/search/query/is_junk/{date}/{page} で日付とページを受け取り、その日に「ゴミ」とマークされた人物検出のクエリ ID 一覧とページングを JSON で返す API を提供する。評価用。認証済み管理クライアントのみ。成功時は 200。
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
    指定日に「ゴミ」とマークされた人物検出のクエリ ID 一覧取得 API を担当するプレゼンテーション。

    POST /person/snapshot/search/query/is_junk/{date}/{page} で日付とページを送信し、該当日のゴミクエリ ID 一覧と total_items・total_pages を取得する。成功時は 200 と person_snapshot_query_ids, pagination を返す。Bearer トークン必須。
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
        指定日のゴミクエリ ID 一覧とページングを取得し、JSON で返す。

        パスの date と page を DTO に渡し、アプリケーション層で search_query_is_junk と search_query_is_junk_paging を呼び、該当 ID 一覧とページング情報をレスポンスに含める。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationUtilPathDate date: 対象日（パス: .../is_junk/{date}/{page}）
        :param PresentationUtilPathInt page: ページ番号
        :param ApplicationPersonSnapshotSearch application: 人物検出検索アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と person_snapshot_query_ids, pagination
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
