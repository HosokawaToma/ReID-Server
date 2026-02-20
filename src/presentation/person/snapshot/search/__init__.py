"""
人物検出検索のプレゼンテーション層

POST /person/snapshot/search/{page} でページ番号と検索条件（ID・カメラ・ビュー・ゴミフラグ・人物ID・時刻範囲・ソート）を受け取り、
人物検出一覧と総件数・ページング情報を JSON で返す API を提供する。認証済み管理クライアントのみ利用可能。成功時は 200。
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
    """
    人物検出検索 API のリクエストボディを保持する DTO。

    検索条件として ID 一覧（ids）、カメラ ID 一覧（camera_ids）、ビュー ID 一覧（view_ids）、ゴミフラグ（is_junk）、
    人物 ID 一覧（person_ids）、撮影時刻範囲（timestamp_after, timestamp_before）、ソート順（sort_by_list）を任意で指定する。すべて省略可能。
    """
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
    人物検出検索の API エンドポイントを担当するプレゼンテーション。

    POST /person/snapshot/search/{page} でページ番号（パス）とボディの検索条件を送信し、
    該当する人物検出結果の一覧と総件数・ページング情報を取得する。成功時は 200 と person_snapshots, total_count 等を返す。Bearer トークン必須。
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
        リクエストの条件とページ番号で人物検出を検索し、一覧とページング情報を JSON で返す。

        ボディが None の場合はクエリを None にし、全件対象のうち指定ページを取得する。アプリケーション層で search と search_paging を呼び、
        person_snapshots 配列と pagination（total_items, total_pages）をレスポンスに含める。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationUtilPathInt page: ページ番号（パス: /person/snapshot/search/{page}）
        :param PresentationPersonSnapshotSearchRequestBody request: 検索条件（None の場合は全件）
        :param ApplicationPersonSnapshotSearch application: 人物検出検索アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と person_snapshots, pagination を含む JSON
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
