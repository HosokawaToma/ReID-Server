from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.request import PresentationUtilRequestBody
from applications.person.snapshot.refresh.detect_junk import ApplicationPersonSnapshotRefreshDetectJunk
from logger import Logger
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from datetime import datetime
import uuid

class PresentationPersonSnapshotRefreshDetectJunkRequest(PresentationUtilRequestBody):
    ids: list[uuid.UUID] | None = None
    person_ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    is_junk: bool | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

class PresentationPersonSnapshotRefreshDetectJunk(PresentationUtilBase):
    router_path = "/person/snapshot/refresh/detect_junk"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Refresh person snapshot detect junk"
    description = "Refresh person snapshot detect junk"
    responses = {
        200: {
            "description": "Person snapshot detect junk refreshed",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotRefreshDetectJunk":
        return cls(
            logger=Logger("presentation_person_snapshot_refresh_detect_junk"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotRefreshDetectJunkRequest | None = None,
        application: ApplicationPersonSnapshotRefreshDetectJunk = get_application(ApplicationPersonSnapshotRefreshDetectJunk),
    ):
        query = None
        if request is not None:
            query = DtoPersonSnapshotQuery(
                ids=request.ids,
                person_ids=request.person_ids,
                camera_ids=request.camera_ids,
                view_ids=request.view_ids,
                is_junk=request.is_junk,
                timestamp_after=request.timestamp_after,
                timestamp_before=request.timestamp_before,
            )
        application.refresh(query=query)
        return PresentationUtilJSONResponse(status=200, content={"message": "Person snapshot detect junk refreshed"})
