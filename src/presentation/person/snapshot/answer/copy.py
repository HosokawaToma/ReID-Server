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
    person_snapshot_ids: list[uuid.UUID]


class PresentationPersonSnapshotAnswerCopy(PresentationUtilBase):
    router_path = "/person/snapshot/answer/copy"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Assign new person ID to person snapshots"
    description = "Assign the same new person ID to multiple person snapshots"
    responses = {
        200: {
            "description": "New person ID assigned successfully",
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
        人物検出結果に新しい人物IDを割り当てる
        :param PresentationUtilAdminClientAuthenticated admin_client_id: 管理者クライアントID
        :param PresentationPersonSnapshotAnswerCopyRequestBody request: リクエストボディ
        :param ApplicationPersonSnapshotAnswerCopy application: アプリケーション
        :return PresentationUtilJSONResponse: レスポンス
        """
        new_person_id = application.assign_new_person_id(
            person_snapshot_ids=DomainIdSequence(items=[DomainId(id=snapshot_id) for snapshot_id in request.person_snapshot_ids]),
        )
        return PresentationUtilJSONResponse(
            status=200,
            content={
                "message": "New person ID assigned successfully",
                "person_id": str(new_person_id.id),
            },
        )
