from presentation import PresentationBase
from presentation import PresentationRequestBody
from presentation import PresentationAdminClientAuthenticated
from presentation import get_application
from presentation import PresentationJSONResponse
from applications.person.snapshot.answer.copy import ApplicationPersonSnapshotAnswerCopy
from dto.id import DtoId
import uuid
from logger import Logger

class PresentationPersonSnapshotAnswerCopyRequestBody(PresentationRequestBody):
    source_person_snapshot_id: uuid.UUID
    target_person_snapshot_ids: list[uuid.UUID]

class PresentationPersonSnapshotAnswerCopy(PresentationBase):
    router_path = "/person/snapshot/answer/copy"
    methods = ["POST"]
    tags = ["Person Snapshot Answer"]
    summary = "Copy a person snapshot answer"
    description = "Copy a person snapshot answer"
    responses = {
        200: {"description": "Person snapshot answer copied"},
        400: {"description": "Bad request"},
    }

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotAnswerCopy":
        return cls(
            logger=Logger("presentation_person_snapshot_answer_copy"),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        body: PresentationPersonSnapshotAnswerCopyRequestBody,
        request: PresentationPersonSnapshotAnswerCopyRequestBody,
        application: ApplicationPersonSnapshotAnswerCopy = get_application(ApplicationPersonSnapshotAnswerCopy),
    ):
        answer_annotation_only_list = application.copy(
            source_person_snapshot_id=DtoId(id=body.source_person_snapshot_id),
            target_person_snapshot_ids=[DtoId(id=id) for id in body.target_person_snapshot_ids],
        )
        return PresentationJSONResponse(status=200, content={
            "target_person_snapshot_answer_annotation_only_list": [
                {
                    "id": str(answer_annotation_only.id),
                    "person_id": str(answer_annotation_only.person_id),
                    "is_junk": answer_annotation_only.is_junk,
                }
                for answer_annotation_only in answer_annotation_only_list
            ]
        })
