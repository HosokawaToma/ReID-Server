"""
人物フロー検索のプレゼンテーション層

POST /person/flow/search で人物 ID と任意の時刻範囲を受け取り、カメラ間の移動（フロー）一覧を JSON で返す API を提供する。
認証済み管理クライアントのみ利用可能。レスポンスには person_id、始点・終点のカメラ ID とタイムスタンプを含む。成功時は 200。
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
    人物フロー検索 API のリクエストボディを保持する DTO。

    人物 ID（person_id）を必須とし、時刻範囲（timestamp_after, timestamp_before）を任意で指定する。
    範囲を省略した場合は該当人物の全フローを返す。
    """
    person_id: uuid.UUID
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None


class PresentationPersonFlowSearch(PresentationUtilBase):
    """
    人物フロー検索の API エンドポイントを担当するプレゼンテーション。

    POST /person/flow/search で人物 ID と任意の時刻範囲を送信し、該当する人物のカメラ間移動（フロー）一覧を取得する。
    各フローは source_camera_id, target_camera_id と source/target_timestamp で表される。成功時は 200 と person_flows 配列を返す。Bearer トークン必須。
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
        リクエストの人物 ID・時刻範囲で人物フローを検索し、一覧を JSON で返す。

        ボディから検索条件を DTO に組み立て、アプリケーション層の search でフロー一覧を取得する。
        レスポンスには各フローの person_id、始点・終点のカメラ ID とタイムスタンプ（ISO 形式）を含める。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationPersonFlowSearchRequestBody body: 人物 ID と任意の時刻範囲
        :param ApplicationPersonFlowSearch application: 人物フロー検索アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と {"person_flows": [{ person_id, source_camera_id, target_camera_id, ... }]}
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
