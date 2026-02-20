"""
人物検出更新のプレゼンテーション層

POST /person/snapshot/refresh で条件（時刻範囲・カメラID・ビューID）を受け取り、該当する人物検出結果の ID を再同定キューに一括投入する API を提供する。
認証済み管理クライアントのみ利用可能。ボディが None または条件未指定の場合は該当する全件を投入する。成功時は 200 とメッセージを JSON で返す。
"""
from presentation.utils.base import PresentationUtilBase
from presentation.utils.request import PresentationUtilRequestBody
from presentation.utils.response import PresentationUtilJSONResponse
from applications.person.snapshot.refresh import ApplicationPersonSnapshotRefresh
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from logger import Logger
from datetime import datetime
from presentation.utils.factory import get_application


class PresentationPersonSnapshotRefreshRequest(PresentationUtilRequestBody):
    """
    人物検出更新（再同定キュー投入）API のリクエストボディを保持する DTO。

    時刻範囲（timestamp_after, timestamp_before）、カメラ ID 一覧（camera_ids）、ビュー ID 一覧（view_ids）を任意で指定する。
    すべて省略可能。省略時は該当する全人物検出結果が再同定キューに投入される。
    """
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None


class PresentationPersonSnapshotRefresh(PresentationUtilBase):
    """
    人物検出更新の API エンドポイントを担当するプレゼンテーション。

    POST /person/snapshot/refresh でリクエストボディの条件に合う人物検出結果の ID を再同定キューに一括投入する。
    バックグラウンドワーカーがキューから取り出して再同定処理を行う。成功時は 200 と {"message": "Person snapshots refreshed"} を返す。Bearer トークン必須。
    """
    router_path = "/person/snapshot/refresh"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Refresh person snapshots"
    description = "Refresh person snapshots"
    responses = {
        200: {
            "description": "Person snapshots refreshed",
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
    def create(cls) -> "PresentationPersonSnapshotRefresh":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotRefresh: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_snapshot_refresh"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotRefreshRequest | None = None,
        application: ApplicationPersonSnapshotRefresh = get_application(
            ApplicationPersonSnapshotRefresh),
    ):
        """
        リクエストの条件に合う人物検出結果の ID を再同定キューに投入し、成功メッセージを JSON で返す。

        リクエストが None または条件未指定の場合はクエリを None にし、アプリケーション層で該当する全 ID をキューに投入する。
        条件指定時は時刻範囲・カメラID・ビューIDでフィルタした結果の ID のみ投入する。投入完了後に 200 を返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationPersonSnapshotRefreshRequest request: 更新対象の条件（None の場合は全件）
        :param ApplicationPersonSnapshotRefresh application: 人物検出更新（再同定キュー投入）アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と {"message": "Person snapshots refreshed"}
        """
        query = None
        if request is not None:
            query = DtoPersonSnapshotQuery(
                timestamp_after=request.timestamp_after,
                timestamp_before=request.timestamp_before,
                camera_ids=request.camera_ids,
                view_ids=request.view_ids,
            )
        application.refresh(query=query)
        return PresentationUtilJSONResponse(status=200, content={"message": "Person snapshots refreshed"})
