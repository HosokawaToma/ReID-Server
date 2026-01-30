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
    source_person_snapshot_id: uuid.UUID
    target_person_snapshot_ids: list[uuid.UUID]

class PresentationPersonSnapshotAnswerAssign(PresentationUtilBase):
    router_path = "/person/snapshot/answer/assign"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Assign answer label to person snapshot"
    description = "Assign answer label to person snapshot"
    responses = {
        200: {"description": "Answer label assigned"},
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotAnswerAssign":
        return cls(
            logger=Logger("presentation_person_snapshot_answer_assign"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotAnswerAssignRequest,
        application: ApplicationPersonSnapshotAnswerAssign = get_application(ApplicationPersonSnapshotAnswerAssign),
    ):
        application.assign(
            source_person_snapshot_id=DtoId(id=request.source_person_snapshot_id),
            target_person_snapshot_ids=[
                DtoId(id=target_person_snapshot_id)
                for target_person_snapshot_id in request.target_person_snapshot_ids
            ],
        )
        return PresentationUtilJSONResponse(status=200, content={"message": "Answer label assigned"})
