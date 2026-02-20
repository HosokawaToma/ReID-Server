"""
人物検出検索のプレゼンテーション層

ページとリクエストボディで条件を指定し、人物検出一覧とページングをJSONで返す。
"""
from applications.person.snapshot.search import ApplicationPersonSnapshotSearch
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from dto.person.snapshot.query import DtoPersonSnapshotQuerySortByKey
from presentation.utils.base import PresentationUtilBase
from presentation.utils.request import PresentationUtilRequestBody
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.type import PresentationUtilPathInt
from presentation.utils.factory import get_application
from logger import Logger
from datetime import datetime
import uuid
from enum import Enum


class PresentationPersonSnapshotSearchSortByKey(str, Enum):
    """人物検出検索のソートキー。"""
    TIMESTAMP_ASC = "timestamp_asc"
    TIMESTAMP_DESC = "timestamp_desc"


class PresentationPersonSnapshotSearchRequestBody(PresentationUtilRequestBody):
    """人物検出検索APIのリクエストボディ。"""
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    is_junk: bool | None = None
    person_ids: list[uuid.UUID] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    sort_by_list: list[PresentationPersonSnapshotSearchSortByKey] | None = None


class PresentationPersonSnapshotSearch(PresentationUtilBase):
    """
    人物検出検索のAPIエンドポイントを提供するプレゼンテーションクラス。
    """
    router_path = "/person/snapshot/search/{page}"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshots"
    description = "Search person snapshots"
    responses = {
        200: {
            "description": "Person snapshots found",
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
    def create(cls) -> "PresentationPersonSnapshotSearch":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotSearch: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_snapshot_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        page: PresentationUtilPathInt,
        request: PresentationPersonSnapshotSearchRequestBody | None = None,
        application: ApplicationPersonSnapshotSearch = get_application(
            ApplicationPersonSnapshotSearch),
    ):
        """
        リクエストの条件で人物検出を検索し、一覧とページングをJSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationUtilPathInt page: ページ番号
        :param PresentationPersonSnapshotSearchRequestBody request: 検索条件（Noneの場合は全件）
        :param ApplicationPersonSnapshotSearch application: 人物検出検索アプリケーション
        :return PresentationUtilJSONResponse: 人物検出一覧とページングを含むJSONレスポンス
        """
        query = None
        if request is not None:
            query = DtoPersonSnapshotQuery(
                ids=request.ids,
                camera_ids=request.camera_ids,
                view_ids=request.view_ids,
                is_junk=request.is_junk,
                person_ids=request.person_ids,
                timestamp_after=request.timestamp_after,
                timestamp_before=request.timestamp_before,
                sort_by_list=[
                    DtoPersonSnapshotQuerySortByKey(sort_by.value)
                    for sort_by in request.sort_by_list
                ] if request.sort_by_list is not None else None,
            )
        items = application.search(
            query=query,
            page=page,
        )
        paging = application.search_paging(query=query)
        return PresentationUtilJSONResponse(
            status=200,
            content={
                "person_snapshots": [
                    {
                        "id": str(item.id),
                        "camera_id": item.camera_id,
                        "view_id": item.view_id,
                        "timestamp": item.timestamp.isoformat(),
                        "is_junk": item.is_junk,
                        "person_id": str(item.person_id),
                    } for item in items
                ],
                "pagination": {
                    "total_items": paging.total_items,
                    "total_pages": paging.total_pages,
                },
            }
        )
