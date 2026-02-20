"""
人物フロー重み検索のプレゼンテーション層

時刻範囲でカメラ間の重み一覧を検索し、JSONで返す。
"""
from applications.person.flow.weight.search import ApplicationPersonFlowWeightSearch
from dto.person.flow.weight.query import DtoPersonFlowWeightQuery
from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from logger import Logger
from presentation.utils.request import PresentationUtilRequestBody
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PresentationPersonFlowWeightSearchRequestBody(PresentationUtilRequestBody):
    """人物フロー重み検索APIのリクエストボディ。"""
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None


class PresentationPersonFlowWeightSearch(PresentationUtilBase):
    """
    人物フロー重み検索のAPIエンドポイントを提供するプレゼンテーションクラス。
    """
    router_path = "/person/flow/weight/search"
    methods = ["POST"]
    tags = ["Person Flow"]
    summary = "Search person flow weight"
    description = "Search person flow weight"
    responses = {
        200: {
            "description": "Person flow weight",
        }
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
    def create(cls) -> "PresentationPersonFlowWeightSearch":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonFlowWeightSearch: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_flow_weight_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        body: PresentationPersonFlowWeightSearchRequestBody | None = None,
        application: ApplicationPersonFlowWeightSearch = get_application(
            ApplicationPersonFlowWeightSearch),
    ):
        """
        リクエストの条件でフロー重みを検索し、一覧をJSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationPersonFlowWeightSearchRequestBody body: 検索条件（Noneの場合は全件）
        :param ApplicationPersonFlowWeightSearch application: フロー重み検索アプリケーション
        :return PresentationUtilJSONResponse: 重み一覧を含むJSONレスポンス
        """
        query = None
        if body is not None:
            query = DtoPersonFlowWeightQuery(
                timestamp_after=body.timestamp_after,
                timestamp_before=body.timestamp_before,
            )
        items = application.search(query=query)
        return PresentationUtilJSONResponse(
            status=200,
            content={
                "weights": [
                    {
                        "target_camera_id": item.target_camera_id,
                        "source_camera_id": item.source_camera_id,
                        "weight": item.weight,
                    } for item in items
                ]
            },
        )
