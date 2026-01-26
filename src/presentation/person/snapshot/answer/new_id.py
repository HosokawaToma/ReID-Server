from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.request import PresentationUtilRequestBody
from presentation.utils.response import PresentationUtilJSONResponse
from logger import Logger
from applications.person.snapshot.answer.new_id import ApplicationPersonSnapshotAnswerNewId
from dto.id import DtoId
from dto.person.id import DtoPersonId
import uuid


class PresentationPersonSnapshotAnswerNewIdRequestBody(PresentationUtilRequestBody):
    person_snapshot_ids: list[uuid.UUID]
    person_id: uuid.UUID | None = None
    is_junk: bool


class PresentationPersonSnapshotAnswerNewId(PresentationUtilBase):
    router_path = "/person/snapshot/answer/new_id"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Update person snapshot answer with new ID"
    description = "Update person snapshot answer with new ID"
    responses = {
        200: {
            "description": "Person snapshot answer updated",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotAnswerNewId":
        return cls(
            logger=Logger("presentation_person_snapshot_answer_new_id"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotAnswerNewIdRequestBody,
        application: ApplicationPersonSnapshotAnswerNewId = get_application(ApplicationPersonSnapshotAnswerNewId),
    ):
        application.new_id(
            person_snapshot_ids=[DtoId(id=person_snapshot_id) for person_snapshot_id in request.person_snapshot_ids],
            person_id=DtoPersonId(
                id=request.person_id,
                is_junk=request.is_junk,
            ),
        )
        return PresentationUtilJSONResponse(
            status=200,
            content={
                "message": "Person snapshot answer updated",
            },
        )
