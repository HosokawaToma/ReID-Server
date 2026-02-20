"""
人物検出正解ラベル割当のプレゼンテーション層

POST /person/snapshot/answer/assign でソース 1 件とターゲット複数件の人物検出 ID を受け取り、
ソースに紐づく正解ラベル（person_id）をターゲットに一括でコピーする API を提供する。認証済み管理クライアントのみ利用可能。成功時は 200。
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
    正解ラベル割当 API のリクエストボディを保持する DTO。

    正解ラベルをコピー元とする人物検出 ID（source_person_snapshot_id）を 1 件と、
    コピー先とする人物検出 ID のリスト（target_person_snapshot_ids）を必須で指定する。いずれも UUID。
    """
    source_person_snapshot_id: uuid.UUID
    target_person_snapshot_ids: list[uuid.UUID]


class PresentationPersonSnapshotAnswerAssign(PresentationUtilBase):
    """
    正解ラベル割当の API エンドポイントを担当するプレゼンテーション。

    POST /person/snapshot/answer/assign でソースの人物検出 ID に紐づく正解ラベル（person_id）を、
    ターゲットの人物検出 ID 群に一括で割り当てる。評価用の正解データ整備に用いる。成功時は 200 と {"message": "Answer label assigned"} を返す。Bearer トークン必須。
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
        ソースの正解ラベルをターゲットに一括割り当てし、成功メッセージを JSON で返す。

        リクエストの source_person_snapshot_id に紐づく person_id を、target_person_snapshot_ids の各 ID にコピーする。
        アプリケーション層で DB 更新を行う。ソースまたはターゲットが存在しない場合は NotFoundError により 404 となる。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationPersonSnapshotAnswerAssignRequest request: ソース 1 件・ターゲット複数件の人物検出 ID
        :param ApplicationPersonSnapshotAnswerAssign application: 正解ラベル割当アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と {"message": "Answer label assigned"}
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
