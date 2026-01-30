from presentation.utils.base import PresentationUtilBase
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.type import PresentationUtilPathInt, PresentationUtilPathUUID
from presentation.utils.factory import get_application
from logger import Logger
from applications.person.snapshot.search.nearest import ApplicationPersonSnapshotSearchNearest
from dto.id import DtoId

class PresentationPersonSnapshotSearchNearest(PresentationUtilBase):
    router_path = "/person/snapshot/search/nearest/{person_snapshot_id}/{page}"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search nearest person snapshots"
    description = "Search nearest person snapshots"
    responses = {
        200: {
            "description": "Person snapshots found",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotSearchNearest":
        return cls(
            logger=Logger("presentation_person_snapshot_search_nearest"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        person_snapshot_id: PresentationUtilPathUUID,
        page: PresentationUtilPathInt,
        application: ApplicationPersonSnapshotSearchNearest = get_application(ApplicationPersonSnapshotSearchNearest),
    ):
        items = application.search(person_snapshot_id=DtoId(id=person_snapshot_id), page=page)
        pagination = application.search_paging(person_snapshot_id=DtoId(id=person_snapshot_id))
        return PresentationUtilJSONResponse(status=200, content={
            "person_snapshots": [
                {
                    "id": str(item.id),
                    "camera_id": item.camera_id,
                    "view_id": item.view_id,
                    "timestamp": item.timestamp.isoformat(),
                    "is_junk": item.is_junk,
                    "person_id": str(item.person_id) if item.person_id is not None else None,
                } for item in items
            ],
            "pagination": {
                "total_items": pagination.total_items,
                "total_pages": pagination.total_pages,
            },
        })
