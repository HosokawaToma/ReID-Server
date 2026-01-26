from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.request import PresentationUtilRequestBody
from presentation.utils.response import PresentationUtilJSONResponse
from logger import Logger
from applications.person.snapshot.answer.copy import ApplicationPersonSnapshotAnswerCopy
from domain.id import DomainId
from domain.id_sequence import DomainIdSequence
import uuid


class PresentationPersonSnapshotAnswerCopyRequestBody(PresentationUtilRequestBody):
    source_id: uuid.UUID
    target_ids: list[uuid.UUID]


class PresentationPersonSnapshotAnswerCopy(PresentationUtilBase):
    router_path = "/person/snapshot/answer/copy"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Copy person snapshot answer"
    description = "Copy person snapshot answer"
    responses = {
        200: {
            "description": "Person snapshot answer copied",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotAnswerCopy":
        return cls(
            logger=Logger("presentation_person_snapshot_answer_copy"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotAnswerCopyRequestBody,
        application: ApplicationPersonSnapshotAnswerCopy = get_application(ApplicationPersonSnapshotAnswerCopy),
    ):
        """
        人物検出結果の正解ラベルをコピーする
        :param PresentationUtilAdminClientAuthenticated admin_client_id: 管理者クライアントID
        :param PresentationPersonSnapshotAnswerCopyRequestBody request: リクエストボディ
        :param ApplicationPersonSnapshotAnswerCopy application: アプリケーション
        :return PresentationUtilJSONResponse: レスポンス
        :raises NotFoundError: コピー元の正解ラベルが見つからない場合に発生するエラー
        """
        application.copy(
            source_id=DomainId(id=request.source_id),
            target_ids=DomainIdSequence(items=[DomainId(id=target_id) for target_id in request.target_ids]),
        )
        return PresentationUtilJSONResponse(
            status=200,
            content={"message": "Person snapshot answer copied"},
        )
