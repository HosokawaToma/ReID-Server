from applications.person.snapshot.search import ApplicationPersonSnapshotSearch
from applications.person.snapshot.search import ApplicationPersonSnapshotSearchFilters
from applications.person.snapshot.search import ApplicationPersonSnapshotSearchOrdering
from presentation import PresentationBase, PresentationRequestBody
from presentation import PresentationAdminClientAuthenticated
from presentation import PresentationJSONResponse
from logger import Logger
from datetime import datetime
import uuid
from presentation import get_application

class PresentationPersonSnapshotSearchFilters(PresentationRequestBody):
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    person_ids: list[uuid.UUID] | None = None
    is_junk: bool | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None


class PresentationPersonSnapshotSearchOrdering(PresentationRequestBody):
    timestamp_asc: bool | None = None
    timestamp_desc: bool | None = None


class PresentationPersonSnapshotSearchRequest(PresentationRequestBody):
    filters: PresentationPersonSnapshotSearchFilters | None = None
    ordering: PresentationPersonSnapshotSearchOrdering | None = None


class PresentationPersonSnapshotSearch(PresentationBase):
    router_path = "/person/snapshot/search"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshots"
    description = "Search person snapshots"
    responses = {
        200: {
            "description": "Person snapshots found",
        },
    }

    def __init__(
        self,
        logger: Logger,
    ):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotSearch":
        return cls(
            logger=Logger("presentation_person_snapshot_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationPersonSnapshotSearchRequest | None = None,
        application: ApplicationPersonSnapshotSearch = get_application(ApplicationPersonSnapshotSearch),
    ):
        filters = None
        if request is not None and request.filters is not None:
            filters = ApplicationPersonSnapshotSearchFilters(
                ids=request.filters.ids,
                camera_ids=request.filters.camera_ids,
                view_ids=request.filters.view_ids,
                person_ids=request.filters.person_ids,
                is_junk=request.filters.is_junk,
                timestamp_after=request.filters.timestamp_after,
                timestamp_before=request.filters.timestamp_before,
            )
        ordering = None
        if request is not None and request.ordering is not None:
            ordering = ApplicationPersonSnapshotSearchOrdering(
                timestamp_asc=request.ordering.timestamp_asc,
                timestamp_desc=request.ordering.timestamp_desc,
            )
        items = await self.run_sync(
            application.search,
            filters=filters,
            ordering=ordering,
        )
        return PresentationJSONResponse(
            status=200,
            content={
                "person_snapshots": [
                    {
                        "id": str(item.id),
                        "camera_id": item.camera_id,
                        "view_id": item.view_id,
                        "timestamp": item.timestamp.isoformat(),
                        "is_junk": item.is_junk,
                        "person_id": str(item.person_id),
                    } for item in items
                ],
            },
        )
