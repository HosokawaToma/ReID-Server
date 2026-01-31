from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from logger import Logger
from applications.person.snapshot.refresh.feature_extract import ApplicationPersonSnapshotRefreshFeatureExtract
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.request import PresentationUtilRequestBody
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from datetime import datetime
import uuid


class PresentationPersonSnapshotRefreshRequest(PresentationUtilRequestBody):
    ids: list[uuid.UUID] | None = None
    person_ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    is_junk: bool | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

class PresentationPersonSnapshotRefreshFeatureExtract(PresentationUtilBase):
    router_path = "/person/snapshot/refresh/feature_extract"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Refresh person snapshot feature extract"
    description = "Refresh person snapshot feature extract"
    responses = {
        200: {
            "description": "Person snapshot feature extract refreshed",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotRefreshFeatureExtract":
        return cls(
            logger=Logger("presentation_person_snapshot_refresh_feature_extract"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationPersonSnapshotRefreshRequest | None = None,
        application: ApplicationPersonSnapshotRefreshFeatureExtract = get_application(ApplicationPersonSnapshotRefreshFeatureExtract),
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
        return PresentationUtilJSONResponse(status=200, content={"message": "Person snapshot feature extract refreshed"})
