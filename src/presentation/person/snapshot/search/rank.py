from presentation.utils.base import PresentationUtilBase
from presentation.utils.request import PresentationUtilRequestBody
from dto.id import DtoId
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from logger import Logger
from applications.person.snapshot.search.rank import ApplicationPersonSnapshotSearchRank
import uuid

class PresentationPersonSnapshotSearchRankRequestBody(PresentationUtilRequestBody):
    person_snapshot_id: uuid.UUID
    limit: int | None = None

class PresentationPersonSnapshotSearchRank(PresentationUtilBase):
    router_path = "/person/snapshot/search/rank"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshot rank"
    description = "Search person snapshots with similar features from different cameras on the same date"
    responses = {
        200: {
            "description": "Person snapshot rank found",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotSearchRank":
        return cls(
            logger=Logger("presentation_person_snapshot_search_rank"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotSearchRankRequestBody,
        application: ApplicationPersonSnapshotSearchRank = get_application(ApplicationPersonSnapshotSearchRank),
    ):
        items = application.search(
            person_snapshot_id=DtoId(id=request.person_snapshot_id),
            limit=request.limit if request.limit is not None else 1,
        )
        return PresentationUtilJSONResponse(status=200, content={
            "person_snapshots": [
                {
                    "id": str(item.id),
                    "camera_id": item.camera_id,
                    "view_id": item.view_id,
                    "timestamp": item.timestamp.isoformat(),
                    "person_id": str(item.person_id) if item.person_id is not None else None,
                    "is_junk": item.is_junk,
                } for item in items
            ]
        })
