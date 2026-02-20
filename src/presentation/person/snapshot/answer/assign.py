"""
人物検出正解ラベル割当のプレゼンテーション層

ソース・ターゲットの人物検出IDを受け取り、正解ラベルを割り当ててJSONで返す。
"""
from presentation.utils.base import PresentationUtilBase
from applications.person.snapshot.answer.assign import ApplicationPersonSnapshotAnswerAssign
from dto.id import DtoId
from logger import Logger
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.request import PresentationUtilRequestBody
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.factory import get_application
import uuid


class PresentationPersonSnapshotAnswerAssignRequest(PresentationUtilRequestBody):
    """
    正解ラベル割当 API のリクエストボディを保持する DTO。ソース1件とターゲット複数件の人物検出IDを必須で指定する。
    """
    source_person_snapshot_id: uuid.UUID
    target_person_snapshot_ids: list[uuid.UUID]


class PresentationPersonSnapshotAnswerAssign(PresentationUtilBase):
    """
    正解ラベル割当の API エンドポイントを担当するプレゼンテーション。ソースの正解ラベルをターゲットにコピーし、結果を JSON で返す。
    """
    router_path = "/person/snapshot/answer/assign"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Assign answer label to person snapshot"
    description = "Assign answer label to person snapshot"
    responses = {
        200: {"description": "Answer label assigned"},
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotAnswerAssign":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotAnswerAssign: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_snapshot_answer_assign"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotAnswerAssignRequest,
        application: ApplicationPersonSnapshotAnswerAssign = get_application(
            ApplicationPersonSnapshotAnswerAssign),
    ):
        """
        ソースの正解ラベルをターゲットに割り当て、成功メッセージをJSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationPersonSnapshotAnswerAssignRequest request: ソース・ターゲットID
        :param ApplicationPersonSnapshotAnswerAssign application: 正解ラベル割当アプリケーション
        :return PresentationUtilJSONResponse: 成功メッセージを含むJSONレスポンス
        """
        application.assign_person_id(
            source_person_snapshot_id=DtoId(
                id=request.source_person_snapshot_id),
            target_person_snapshot_ids=[
                DtoId(id=target_person_snapshot_id)
                for target_person_snapshot_id in request.target_person_snapshot_ids
            ],
        )
        return PresentationUtilJSONResponse(status=200, content={"message": "Answer label assigned"})
