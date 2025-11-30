from applications.person.snapshot.search import ApplicationPersonSnapshotSearch
from applications.person.snapshot.search import ApplicationPersonSnapshotSearchParams
from applications.person.snapshot.search import ApplicationPersonSnapshotSearchFilters
from applications.person.snapshot.search import ApplicationPersonSnapshotSearchOrdering
from presentation import PresentationBase
from presentation import PresentationRequest
from presentation import PresentationResponse
from presentation import PresentationLogger
from environment import Environment
from datetime import datetime
import uuid

class PresentationPersonSnapshotSearchFilters(PresentationRequest):
    ids: list[uuid.UUID] | None = None
    image_ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    person_ids: list[uuid.UUID] | None = None
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None

class PresentationPersonSnapshotSearchOrdering(PresentationRequest):
    timestamp_asc: bool | None = None
    timestamp_desc: bool | None = None

class PresentationPersonSnapshotSearchRequest(PresentationRequest):
    filters: PresentationPersonSnapshotSearchFilters | None = None
    ordering: PresentationPersonSnapshotSearchOrdering | None = None

class PresentationPersonSnapshotSearch(PresentationBase):
    @property
    def router_path(self) -> str:
        return "/person/snapshot/search"

    @property
    def methods(self) -> list[str]:
        return ["POST"]

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
        logger: PresentationLogger,
        application_person_snapshot_search: ApplicationPersonSnapshotSearch,
    ):
        super().__init__(logger=logger)
        self.application_person_snapshot_search = application_person_snapshot_search

    @classmethod
    def create(cls, environment: Environment) -> "PresentationPersonSnapshotSearch":
        return cls(
            logger=PresentationLogger(),
            application_person_snapshot_search=ApplicationPersonSnapshotSearch.create(
                environment=environment,
            ),
        )

    async def handle(
        self,
        request: PresentationPersonSnapshotSearchRequest,
    ) -> PresentationResponse:
        try:
            filters = None
            if request.filters:
                filters = ApplicationPersonSnapshotSearchFilters(
                    ids=request.filters.ids,
                    image_ids=request.filters.image_ids,
                    camera_ids=request.filters.camera_ids,
                    view_ids=request.filters.view_ids,
                    person_ids=request.filters.person_ids,
                    after_timestamp=request.filters.after_timestamp,
                    before_timestamp=request.filters.before_timestamp,
                )
            ordering = None
            if request.ordering:
                ordering = ApplicationPersonSnapshotSearchOrdering(
                    timestamp_asc=request.ordering.timestamp_asc,
                    timestamp_desc=request.ordering.timestamp_desc,
                )
            person_snapshots = self.application_person_snapshot_search.search(
                params=ApplicationPersonSnapshotSearchParams(
                    filters=filters,
                    ordering=ordering,
                )
            )
            self.logger.info(f"Person snapshots found: {len(person_snapshots)}")
            return PresentationResponse(
                status=200,
                content={
                    "person_snapshots": [
                        {
                            "id": str(person_snapshot.id),
                            "image_id": str(person_snapshot.image_id),
                            "camera_id": person_snapshot.camera_id,
                            "view_id": person_snapshot.view_id,
                            "timestamp": person_snapshot.timestamp.isoformat(),
                            "person_id": str(person_snapshot.person_id),
                        } for person_snapshot in person_snapshots
                    ],
                },
            )
        except Exception as e:
            self.logger.error(f"Internal server error: {e}")
            return PresentationResponse(
                status=500,
                content={
                    "message": "Internal server error",
                },
            )
