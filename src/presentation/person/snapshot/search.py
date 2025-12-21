from applications.person.snapshot.search import ApplicationPersonSnapshotSearch
from applications.person.snapshot.search import ApplicationPersonSnapshotSearchFilters
from applications.person.snapshot.search import ApplicationPersonSnapshotSearchOrdering
from presentation import PresentationBase, PresentationRequestBody
from presentation import PresentationAdminClientAuthenticated
from presentation import PresentationJSONResponse
from logger import Logger
from environment import Environment
from datetime import datetime
import uuid

class PresentationPersonSnapshotSearchFilters(PresentationRequestBody):
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    person_ids: list[uuid.UUID] | None = None
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
        application_person_snapshot_search: ApplicationPersonSnapshotSearch,
    ):
        super().__init__(logger=logger)
        self.application_person_snapshot_search = application_person_snapshot_search

    @classmethod
    def create(cls, environment: Environment) -> "PresentationPersonSnapshotSearch":
        return cls(
            logger=Logger("person_snapshot_search"),
            application_person_snapshot_search=ApplicationPersonSnapshotSearch.create(
                environment=environment,
            ),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationPersonSnapshotSearchRequest | None = None,
    ):
        filters = None
        if request is not None and request.filters is not None:
            filters = ApplicationPersonSnapshotSearchFilters(
                ids=request.filters.ids,
                camera_ids=request.filters.camera_ids,
                view_ids=request.filters.view_ids,
                person_ids=request.filters.person_ids,
                timestamp_after=request.filters.timestamp_after,
                timestamp_before=request.filters.timestamp_before,
            )
        ordering = None
        if request is not None and request.ordering is not None:
            ordering = ApplicationPersonSnapshotSearchOrdering(
                timestamp_asc=request.ordering.timestamp_asc,
                timestamp_desc=request.ordering.timestamp_desc,
                )
        items = self.application_person_snapshot_search.search(
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
                        "person_id": str(item.person_id),
                    } for item in items
                ],
            },
        )
