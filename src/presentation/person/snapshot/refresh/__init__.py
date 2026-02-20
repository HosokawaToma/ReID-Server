"""
人物検出更新のプレゼンテーション層

条件（時刻・カメラ等）を受け取り、該当する人物検出を再同定キューに投入してJSONで返す。
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
    人物検出更新（再同定キュー投入）API のリクエストボディを保持する DTO。時刻範囲・カメラ・ビューを任意で指定できる。
    """
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None


class PresentationPersonSnapshotRefresh(PresentationUtilBase):
    """
    人物検出更新の API エンドポイントを担当するプレゼンテーション。条件に合う人物検出を再同定キューに投入し、結果を JSON で返す。
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
        リクエストの条件に合う人物検出を再同定キューに投入し、成功メッセージをJSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationPersonSnapshotRefreshRequest request: 更新条件（Noneの場合は全件対象）
        :param ApplicationPersonSnapshotRefresh application: 人物検出更新アプリケーション
        :return PresentationUtilJSONResponse: 成功メッセージを含むJSONレスポンス
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
