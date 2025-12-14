from presentation import PresentationBase, PresentationLogger, PresentationJSONResponse, PresentationRequest
from applications.person.snapshot.refresh import ApplicationPersonSnapshotRefresh
from applications.person.snapshot.refresh import ApplicationPersonSnapshotRefreshParams
from presentation import PresentationAdminClientAuthenticated
from environment import Environment
from datetime import datetime

class PresentationPersonSnapshotRefreshRequest(PresentationRequest):
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
        logger: PresentationLogger,
        application: ApplicationPersonSnapshotRefresh,
    ):
        super().__init__(logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "PresentationPersonSnapshotRefresh":
        return cls(
            logger=PresentationLogger(),
            application=ApplicationPersonSnapshotRefresh.create(
                environment=environment,
            ),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationPersonSnapshotRefreshRequest,
    ):
        self.application.refresh(
            ApplicationPersonSnapshotRefreshParams(
                timestamp_after=request.timestamp_after,
                timestamp_before=request.timestamp_before,
                camera_ids=request.camera_ids,
                view_ids=request.view_ids,
            )
        )
        return PresentationJSONResponse(status=200, content={"message": "Person snapshots refreshed"})
