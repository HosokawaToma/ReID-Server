"""
人物フロー検索のプレゼンテーション層

人物ID・時刻範囲でフローを検索し、一覧をJSONで返す。
"""
from presentation.utils.base import PresentationUtilBase
from presentation.utils.factory import get_application
from presentation.utils.request import PresentationUtilRequestBody
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from applications.person.flow.search import ApplicationPersonFlowSearch
from dto.person.flow.query import DtoPersonFlowQuery
from logger import Logger
from datetime import datetime
import uuid


class PresentationPersonFlowSearchRequestBody(PresentationUtilRequestBody):
    """
    人物フロー検索 API のリクエストボディを保持する DTO。人物ID・タイムスタンプ範囲を任意で指定できる。
    """
    person_id: uuid.UUID
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None


class PresentationPersonFlowSearch(PresentationUtilBase):
    """
    人物フロー検索の API エンドポイントを担当するプレゼンテーション。人物ID・時刻範囲でフロー一覧を JSON で返す。
    """
    router_path = "/person/flow/search"
    methods = ["POST"]
    tags = ["Person Flow"]
    summary = "Search person flows"
    description = "Search person flows"
    responses = {
        200: {
            "description": "Person flows",
            "content": {"application/json": {"example": [{"id": "123e4567-e89b-12d3-a456-426614174000", "name": "John Doe"}]}},
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
    def create(cls) -> "PresentationPersonFlowSearch":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonFlowSearch: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_flow_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        body: PresentationPersonFlowSearchRequestBody,
        application: ApplicationPersonFlowSearch = get_application(
            ApplicationPersonFlowSearch),
    ):
        """
        リクエストの条件で人物フローを検索し、一覧をJSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationPersonFlowSearchRequestBody body: 検索条件
        :param ApplicationPersonFlowSearch application: 人物フロー検索アプリケーション
        :return PresentationUtilJSONResponse: 人物フロー一覧を含むJSONレスポンス
        """
        query = DtoPersonFlowQuery(
            person_id=body.person_id,
            timestamp_after=body.timestamp_after,
            timestamp_before=body.timestamp_before,
        )
        items = application.search(query=query)
        return PresentationUtilJSONResponse(status=200, content={
            "person_flows": [
                {
                    "person_id": str(item.person_id),
                    "source_camera_id": item.source_camera_id,
                    "target_camera_id": item.target_camera_id,
                    "source_timestamp": item.source_timestamp.isoformat(),
                    "target_timestamp": item.target_timestamp.isoformat(),
                } for item in items
            ],
        })
