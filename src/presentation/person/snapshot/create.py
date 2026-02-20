"""
人物検出作成のプレゼンテーション層

画像・時刻・カメラID・ビューIDを受け取り、人物検出キューに投入してJSONで返す。
"""
from applications.person.snapshot.create import ApplicationPersonSnapshotCreate
from dto.location import DtoLocation
from dto.timestamp import DtoTimestamp
from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.type import PresentationUtilFromImage, PresentationUtilFromDatetime, PresentationUtilFromInt
from presentation.utils.response import PresentationUtilJSONResponse
from logger import Logger
from presentation.utils.factory import get_application


class PresentationPersonSnapshotCreate(PresentationUtilBase):
    """
    人物検出作成のAPIエンドポイントを提供するプレゼンテーションクラス。
    """
    router_path = "/person/snapshot/create"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Create a person snapshot"
    description = "Create a person snapshot"
    responses = {
        200: {"description": "Person snapshot created"},
        400: {"description": "Bad request"},
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
    def create(cls) -> "PresentationPersonSnapshotCreate":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotCreate: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_snapshot_create"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        image: PresentationUtilFromImage,
        timestamp: PresentationUtilFromDatetime,
        camera_id: PresentationUtilFromInt,
        view_id: PresentationUtilFromInt,
        application: ApplicationPersonSnapshotCreate = get_application(
            ApplicationPersonSnapshotCreate),
    ):
        """
        画像・位置・時刻で人物検出をキューに投入し、成功メッセージをJSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationUtilFromImage image: 画像
        :param PresentationUtilFromDatetime timestamp: 時刻
        :param PresentationUtilFromInt camera_id: カメラID
        :param PresentationUtilFromInt view_id: ビューID
        :param ApplicationPersonSnapshotCreate application: 人物検出作成アプリケーション
        :return PresentationUtilJSONResponse: 成功メッセージを含むJSONレスポンス
        """
        application.save(
            location=DtoLocation(camera_id=camera_id, view_id=view_id),
            timestamp=DtoTimestamp(timestamp=timestamp),
            image=image,
        )
        return PresentationUtilJSONResponse(status=200, content={"message": "Person snapshot created"})
