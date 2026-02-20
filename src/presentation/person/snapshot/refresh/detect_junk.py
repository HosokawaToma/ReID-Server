"""
人物検出ジャンク再判定のプレゼンテーション層

条件を受け取り、該当する人物検出をジャンク判定キューに投入してJSONで返す。
"""
from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.request import PresentationUtilRequestBody
from applications.person.snapshot.refresh.detect_junk import ApplicationPersonSnapshotRefreshDetectJunk
from logger import Logger
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from datetime import datetime
import uuid


class PresentationPersonSnapshotRefreshDetectJunkRequest(PresentationUtilRequestBody):
    """
    ジャンク再判定 API のリクエストボディを保持する DTO。ID・人物ID・カメラ・ビュー・ゴミフラグ・時刻範囲を任意で指定できる。
    """
    ids: list[uuid.UUID] | None = None
    person_ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    is_junk: bool | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None


class PresentationPersonSnapshotRefreshDetectJunk(PresentationUtilBase):
    """
    ジャンク再判定の API エンドポイントを担当するプレゼンテーション。条件に合う人物検出をジャンク判定キューに投入し、結果を JSON で返す。
    """
    router_path = "/person/snapshot/refresh/detect_junk"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Refresh person snapshot detect junk"
    description = "Refresh person snapshot detect junk"
    responses = {
        200: {
            "description": "Person snapshot detect junk refreshed",
        },
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotRefreshDetectJunk":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotRefreshDetectJunk: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_snapshot_refresh_detect_junk"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotRefreshDetectJunkRequest | None = None,
        application: ApplicationPersonSnapshotRefreshDetectJunk = get_application(
            ApplicationPersonSnapshotRefreshDetectJunk),
    ):
        """
        リクエストの条件に合う人物検出をジャンク判定キューに投入し、成功メッセージをJSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationPersonSnapshotRefreshDetectJunkRequest request: 条件（Noneの場合は全件対象）
        :param ApplicationPersonSnapshotRefreshDetectJunk application: ジャンク再判定アプリケーション
        :return PresentationUtilJSONResponse: 成功メッセージを含むJSONレスポンス
        """
        query = None
        if request is not None:
            query = DtoPersonSnapshotQuery(
                ids=request.ids,
                person_ids=request.person_ids,
                camera_ids=request.camera_ids,
                view_ids=request.view_ids,
                is_junk=request.is_junk,
                timestamp_after=request.timestamp_after,
                timestamp_before=request.timestamp_before,
            )
        application.refresh(query=query)
        return PresentationUtilJSONResponse(status=200, content={"message": "Person snapshot detect junk refreshed"})
