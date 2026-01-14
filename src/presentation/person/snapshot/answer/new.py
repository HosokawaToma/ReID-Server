from presentation import PresentationBase
from logger import Logger
from presentation import PresentationAdminClientAuthenticated
from presentation import PresentationRequestBody
from presentation import get_application
from presentation import PresentationJSONResponse
from applications.person.snapshot.answer.new import ApplicationPersonSnapshotAnswerNew
from dto.id import DtoId
import uuid


class PresentationPersonSnapshotAnswerNewRequestBody(PresentationRequestBody):
    person_snapshot_ids: list[uuid.UUID]


class PresentationPersonSnapshotAnswerNew(PresentationBase):
    router_path = "/person/snapshot/answer/new"
    methods = ["POST"]
    tags = ["Person Snapshot Answer"]
    summary = "Create a person snapshot answer"
    description = "Create a person snapshot answer"
    responses = {
        200: {"description": "Person snapshot answer created"},
        400: {"description": "Bad request"},
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotAnswerNew":
        return cls(
            logger=Logger("presentation_person_snapshot_answer_new"),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        body: PresentationPersonSnapshotAnswerNewRequestBody,
        request: PresentationPersonSnapshotAnswerNewRequestBody,
        application: ApplicationPersonSnapshotAnswerNew = get_application(ApplicationPersonSnapshotAnswerNew)
    ) -> PresentationJSONResponse:
        answer_only = application.new(
            [
                DtoId(id=id)
                for id in body.person_snapshot_ids
            ]
        )
        return PresentationJSONResponse(status=200, content={
            "person_snapshot_answer_annotations": [
                {
                    "id": answer_only.id,
                    "person_id": answer_only.person_id,
                    "is_junk": answer_only.is_junk,
                }
                for answer_only in answer_only
            ]
        })
