"""
人物検出ジャンク再判定のプレゼンテーション層

POST /person/snapshot/refresh/detect_junk で条件（ID・人物ID・カメラ・ビュー・ゴミフラグ・時刻範囲）を受け取り、該当する人物検出結果の ID をジャンク判定キューに一括投入する API を提供する。認証済み管理クライアントのみ利用可能。条件未指定時は全件対象。成功時は 200。
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
    ジャンク再判定 API のリクエストボディを保持する DTO。

    ID 一覧（ids）、人物 ID 一覧（person_ids）、カメラ ID 一覧（camera_ids）、ビュー ID 一覧（view_ids）、ゴミフラグ（is_junk）、時刻範囲（timestamp_after, timestamp_before）を任意で指定する。すべて省略時は全件がジャンク判定キューに投入される。
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
    ジャンク再判定の API エンドポイントを担当するプレゼンテーション。

    POST /person/snapshot/refresh/detect_junk で条件に合う人物検出結果の ID をジャンク判定キューに一括投入する。バックグラウンドワーカーが YOLO 等で再判定する。成功時は 200 と {"message": "..."} を返す。Bearer トークン必須。
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
        リクエストの条件に合う人物検出結果の ID をジャンク判定キューに投入し、成功メッセージを JSON で返す。

        リクエストが None または条件未指定の場合はクエリを None にし、該当する全 ID をキューに投入する。アプリケーション層でキュー投入後に 200 を返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationPersonSnapshotRefreshDetectJunkRequest request: 対象条件（None の場合は全件）
        :param ApplicationPersonSnapshotRefreshDetectJunk application: ジャンク再判定アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と成功メッセージ
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
