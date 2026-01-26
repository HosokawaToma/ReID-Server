from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.request import PresentationUtilRequestBody
from presentation.utils.response import PresentationUtilJSONResponse
from logger import Logger
from applications.person.snapshot.answer.search import ApplicationPersonSnapshotAnswerSearch
from dto.person.snapshot.answer.query import DtoPersonSnapshotAnswerQuery
from dto.person.snapshot.answer.query import DtoPersonSnapshotAnswerQuerySortByKey
import uuid
from enum import Enum

class PresentationPersonSnapshotAnswerSearchSortByKey(str, Enum):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"

class PresentationPersonSnapshotAnswerSearchRequestBody(PresentationUtilRequestBody):
    person_snapshot_ids: list[uuid.UUID] | None = None
    person_ids: list[uuid.UUID] | None = None
    is_junk: bool | None = None
    sort_by_list: list[PresentationPersonSnapshotAnswerSearchSortByKey] | None = None

class PresentationPersonSnapshotAnswerSearch(PresentationUtilBase):
    router_path = "/person/snapshot/answer/search"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshot answer"
    description = "Search person snapshot answer"
    responses = {
        200: {
            "description": "Person snapshot answer found",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotAnswerSearch":
        return cls(
            logger=Logger("presentation_person_snapshot_answer_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotAnswerSearchRequestBody | None = None,
        application: ApplicationPersonSnapshotAnswerSearch = get_application(ApplicationPersonSnapshotAnswerSearch),
    ):
        query = None
        if request is not None:
            query = DtoPersonSnapshotAnswerQuery(
                person_snapshot_ids=request.person_snapshot_ids,
                person_ids=request.person_ids,
                is_junk=request.is_junk,
                sort_by_list=[
                    DtoPersonSnapshotAnswerQuerySortByKey(sort_by.value)
                    for sort_by in request.sort_by_list
                ] if request.sort_by_list is not None else None,
            )
        items = application.search(query=query)
        return PresentationUtilJSONResponse(
            status=200,
            content={
                "person_snapshot_answers": [
                    {
                        "id": str(item.id),
                        "person_id": str(item.person_id) if item.person_id is not None else None,
                        "is_junk": item.is_junk,
                    } for item in items
                ],
            },
        )
