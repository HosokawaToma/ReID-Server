"""
人物フロー重み検索のプレゼンテーション層

POST /person/flow/weight/search で任意の時刻範囲を受け取り、カメラ間のフロー件数（重み）一覧を JSON で返す API を提供する。
認証済み管理クライアントのみ利用可能。各要素は source_camera_id, target_camera_id, weight で表される。成功時は 200。
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
    """
    人物フロー重み検索 API のリクエストボディを保持する DTO。

    時刻範囲（timestamp_after, timestamp_before）を任意で指定する。省略時は全期間の重みを返す。
    """
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None


class PresentationPersonFlowWeightSearch(PresentationUtilBase):
    """
    人物フロー重み検索の API エンドポイントを担当するプレゼンテーション。

    POST /person/flow/weight/search で時刻範囲を送信し、カメラ間の移動件数（重み）の集計一覧を取得する。
    レスポンスは weights 配列（各要素は source_camera_id, target_camera_id, weight）。成功時は 200。Bearer トークン必須。
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
        リクエストの時刻範囲でフロー重みを検索し、一覧を JSON で返す。

        ボディが None または範囲未指定の場合はクエリを None にし、全期間の重みを取得する。
        アプリケーション層で集計した結果を weights 配列として返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationPersonFlowWeightSearchRequestBody body: 時刻範囲（None の場合は全件）
        :param ApplicationPersonFlowWeightSearch application: フロー重み検索アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と {"weights": [{ source_camera_id, target_camera_id, weight }, ...]}
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
