from presentation.utils.base import PresentationUtilBase
from presentation.utils.request import PresentationUtilRequestBody
from presentation.utils.response import PresentationUtilJSONResponse
from applications.person.snapshot.refresh import ApplicationPersonSnapshotRefresh
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from logger import Logger
from datetime import datetime
from presentation.utils.factory import get_application


class PresentationPersonSnapshotRefreshRequest(PresentationUtilRequestBody):
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None


class PresentationPersonSnapshotRefresh(PresentationUtilBase):
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
    ):
        super().__init__(logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotRefresh":
        return cls(
            logger=Logger("presentation_person_snapshot_refresh"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotRefreshRequest | None = None,
        application: ApplicationPersonSnapshotRefresh = get_application(ApplicationPersonSnapshotRefresh),
    ):
        query = None
        if request is not None:
            query = DtoPersonSnapshotQuery(
                timestamp_after=request.timestamp_after,
                timestamp_before=request.timestamp_before,
                camera_ids=request.camera_ids,
                view_ids=request.view_ids,
            )
        application.refresh(query=query)
        return PresentationUtilJSONResponse(status=200, content={"message": "Person snapshots refreshed"})
