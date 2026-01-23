from applications.camera_frame.search import ApplicationCameraFrameSearch
from presentation import PresentationBase, get_application
from logger import Logger
from presentation import PresentationRequestBody
from dto.camera_frame.query import DtoCameraFrameQuery
from dataclasses import dataclass
from datetime import datetime
from presentation import PresentationJSONResponse
from presentation import PresentationAdminClientAuthenticated
import uuid
from enum import Enum

class PresentationCameraFrameSearchSortByKey(str, Enum):
    TIMESTAMP_ASC = "timestamp_asc"
    TIMESTAMP_DESC = "timestamp_desc"

@dataclass
class PresentationCameraFrameSearchRequestBody(PresentationRequestBody):
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    sort_by_list: list[PresentationCameraFrameSearchSortByKey] | None = None

class PresentationCameraFrameSearch(PresentationBase):
    router_path = "/frame/search"
    methods = ["POST"]
    tags = ["Camera Frame"]
    summary = "Search camera frames"
    description = "Search camera frames"
    responses = {
        200: {
            "description": "Frames",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationCameraFrameSearch":
        return cls(
            logger=Logger("presentation_camera_frame_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationCameraFrameSearchRequestBody | None = None,
        application: ApplicationCameraFrameSearch = get_application(ApplicationCameraFrameSearch),
    ) -> PresentationJSONResponse:
        query = None
        if request is not None:
            query = DtoCameraFrameQuery(
                ids=request.ids,
                camera_ids=request.camera_ids,
                view_ids=request.view_ids,
                timestamp_after=request.timestamp_after,
                timestamp_before=request.timestamp_before,
            )
        camera_frames = application.search(query=query)
        return PresentationJSONResponse(status=200, content={
            "camera_frames": [
                {
                    "id": str(camera_frame.id),
                    "camera_id": camera_frame.camera_id,
                    "view_id": camera_frame.view_id,
                    "timestamp": camera_frame.timestamp.isoformat(),
                } for camera_frame in camera_frames
            ]
        })
