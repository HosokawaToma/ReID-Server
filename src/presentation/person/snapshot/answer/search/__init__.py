"""
人物検出結果の正解ラベル検索のプレゼンテーション層

POST /person/snapshot/answer/search で人物検出 ID・人物 ID・ゴミフラグ・ソート順などの条件を受け取り、
正解ラベル（人物検出と person_id の対応）一覧を JSON で返す API を提供する。認証済み管理クライアントのみ利用可能。成功時は 200。
"""
from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.request import PresentationUtilRequestBody
from presentation.utils.response import PresentationUtilJSONResponse
from logger import Logger
from applications.person.snapshot.answer.search import ApplicationPersonSnapshotAnswerSearch
from dto.person.snapshot.answer.query import DtoPersonSnapshotAnswerQuery
from dto.person.snapshot.answer.query import DtoPersonSnapshotAnswerQuerySortByKey
import uuid
from enum import Enum


class PresentationPersonSnapshotAnswerSearchSortByKey(str, Enum):
    """正解ラベル検索のソートキー。"""
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"


class PresentationPersonSnapshotAnswerSearchRequestBody(PresentationUtilRequestBody):
    """
    正解ラベル検索 API のリクエストボディを保持する DTO。

    人物検出 ID 一覧（person_snapshot_ids）、人物 ID 一覧（person_ids）、ゴミフラグ（is_junk）、ソート順（sort_by_list）を任意で指定する。
    すべて省略可能。省略時は該当する全正解ラベルを返す。
    """
    person_snapshot_ids: list[uuid.UUID] | None = None
    person_ids: list[uuid.UUID] | None = None
    is_junk: bool | None = None
    sort_by_list: list[PresentationPersonSnapshotAnswerSearchSortByKey] | None = None


class PresentationPersonSnapshotAnswerSearch(PresentationUtilBase):
    """
    正解ラベル検索の API エンドポイントを担当するプレゼンテーション。

    POST /person/snapshot/answer/search で検索条件を送信し、人物検出と正解 person_id の対応一覧を取得する。
    評価用の正解データ参照に用いる。成功時は 200 と正解ラベル一覧を返す。Bearer トークン必須。
    """
    router_path = "/person/snapshot/answer/search"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshot answer"
    description = "Search person snapshot answer"
    responses = {
        200: {
            "description": "Person snapshot answer found",
        },
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotAnswerSearch":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotAnswerSearch: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_snapshot_answer_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotAnswerSearchRequestBody | None = None,
        application: ApplicationPersonSnapshotAnswerSearch = get_application(
            ApplicationPersonSnapshotAnswerSearch),
    ):
        """
        リクエストボディの条件で正解ラベルを検索し、結果を JSON で返す。

        リクエストが None または条件未指定の場合はクエリを None にし、全件検索する。
        アプリケーション層で検索した正解ラベル一覧をレスポンスに含める。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationPersonSnapshotAnswerSearchRequestBody request: 検索条件（None の場合は全件）
        :param ApplicationPersonSnapshotAnswerSearch application: 正解ラベル検索アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と正解ラベル一覧（person_snapshot_id と person_id の対応等）
        """
        query = None
        if request is not None:
            query = DtoPersonSnapshotAnswerQuery(
                person_snapshot_ids=request.person_snapshot_ids,
                person_ids=request.person_ids,
                is_junk=request.is_junk,
                sort_by_list=[
                    DtoPersonSnapshotAnswerQuerySortByKey(sort_by.value)
                    for sort_by in request.sort_by_list
                ] if request.sort_by_list is not None else None,
            )
        items = application.search(query=query)
        return PresentationUtilJSONResponse(
            status=200,
            content={
                "person_snapshot_answers": [
                    {
                        "id": str(item.id),
                        "person_id": str(item.person_id) if item.person_id is not None else None,
                        "is_junk": item.is_junk,
                    } for item in items
                ],
            },
        )
