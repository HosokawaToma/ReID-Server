"""
人物検出作成のプレゼンテーション層。

POST /person/snapshot/create で画像・撮影時刻・カメラID・ビューIDを受け取り、
人物検出作成ジョブを登録する API を提供する。認証済み管理クライアントのみ利用可能。
成功時は 200 とメッセージを JSON で返し、不正リクエスト時は 400 を返す。
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
    人物検出作成の API エンドポイントを担当するプレゼンテーション。

    POST /person/snapshot/create で multipart または JSON から画像・撮影時刻・カメラID・ビューIDを受け取り、
    アプリケーション層で人物検出作成ジョブを登録する。実際の検出・再同定はバックグラウンドで行われる。
    成功時は 200 と {"message": "Person snapshot created"} を返す。Bearer トークン必須。
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
        画像・撮影位置・時刻から人物検出作成ジョブを 1 件登録し、成功メッセージを JSON で返す。

        受け取った画像と位置（camera_id, view_id）・時刻を DTO にまとめ、アプリケーション層の save でジョブを登録する。
        実際の人物検出・再同定はバックグラウンドワーカーが非同期で実行され、登録成功時は 200 を返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationUtilFromImage image: アップロードされた画像（multipart または JSON 由来）
        :param PresentationUtilFromDatetime timestamp: 撮影時刻
        :param PresentationUtilFromInt camera_id: 撮影カメラ ID
        :param PresentationUtilFromInt view_id: ビュー ID
        :param ApplicationPersonSnapshotCreate application: 人物検出作成アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と {"message": "Person snapshot created"}
        """
        application.save(
            location=DtoLocation(camera_id=camera_id, view_id=view_id),
            timestamp=DtoTimestamp(timestamp=timestamp),
            image=image,
        )
        return PresentationUtilJSONResponse(status=200, content={"message": "Person snapshot created"})
