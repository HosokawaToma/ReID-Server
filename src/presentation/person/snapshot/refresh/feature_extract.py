from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from logger import Logger
from applications.person.snapshot.refresh.feature_extract import ApplicationPersonSnapshotRefreshFeatureExtract
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.request import PresentationUtilRequestBody
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from datetime import datetime
import uuid


"""
人物検出特徴量再抽出のプレゼンテーション層

条件を受け取り、該当する人物検出を特徴量抽出キューに投入してJSONで返す。
"""


class PresentationPersonSnapshotRefreshRequest(PresentationUtilRequestBody):
    """特徴量再抽出APIのリクエストボディ。"""
    ids: list[uuid.UUID] | None = None
    person_ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    is_junk: bool | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None


class PresentationPersonSnapshotRefreshFeatureExtract(PresentationUtilBase):
    """
    人物検出特徴量再抽出のAPIエンドポイントを提供するプレゼンテーションクラス。
    """
    router_path = "/person/snapshot/refresh/feature_extract"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Refresh person snapshot feature extract"
    description = "Refresh person snapshot feature extract"
    responses = {
        200: {
            "description": "Person snapshot feature extract refreshed",
        },
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotRefreshFeatureExtract":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotRefreshFeatureExtract: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger(
                "presentation_person_snapshot_refresh_feature_extract"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotRefreshRequest | None = None,
        application: ApplicationPersonSnapshotRefreshFeatureExtract = get_application(
            ApplicationPersonSnapshotRefreshFeatureExtract),
    ):
        """
        リクエストの条件に合う人物検出を特徴量抽出キューに投入し、成功メッセージをJSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationPersonSnapshotRefreshRequest request: 条件（Noneの場合は全件対象）
        :param ApplicationPersonSnapshotRefreshFeatureExtract application: 特徴量再抽出アプリケーション
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
        return PresentationUtilJSONResponse(status=200, content={"message": "Person snapshot feature extract refreshed"})
