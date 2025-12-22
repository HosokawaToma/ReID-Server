from presentation import PresentationBase, PresentationJSONResponse, PresentationRequestBody
from applications.person.snapshot.refresh import ApplicationPersonSnapshotRefresh
from applications.person.snapshot.refresh import ApplicationPersonSnapshotRefreshParams
from presentation import PresentationAdminClientAuthenticated
from environment import Environment
from logger import Logger
from datetime import datetime

class PresentationPersonSnapshotRefreshRequest(PresentationRequestBody):
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None

class PresentationPersonSnapshotRefresh(PresentationBase):
    router_path = "/person/snapshot/refresh"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Refresh person snapshots"
    description = "Refresh person snapshots"
    responses = {
        200: {
            "description": "Person snapshots refreshed",
        }
    }

    def __init__(
        self,
        logger: Logger,
        application: ApplicationPersonSnapshotRefresh,
    ):
        super().__init__(logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "PresentationPersonSnapshotRefresh":
        return cls(
            logger=Logger("presentation_person_snapshot_refresh"),
            application=ApplicationPersonSnapshotRefresh.create(
                environment=environment,
            ),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationPersonSnapshotRefreshRequest | None = None,
    ):
        params = None
        if request is not None:
            params = ApplicationPersonSnapshotRefreshParams(
                timestamp_after=request.timestamp_after,
                timestamp_before=request.timestamp_before,
                camera_ids=request.camera_ids,
                view_ids=request.view_ids,
            )
        self.application.refresh(params=params)
        return PresentationJSONResponse(status=200, content={"message": "Person snapshots refreshed"})
