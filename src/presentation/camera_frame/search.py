from applications.camera_frame.search import ApplicationCameraFrameSearch
from presentation.utils.base import PresentationUtilBase
from presentation.utils.factory import get_application
from logger import Logger
from presentation.utils.request import PresentationUtilRequestBody
from dto.camera_frame.query import DtoCameraFrameQuery, DtoCameraFrameQuerySortByKey
from dataclasses import dataclass
from datetime import datetime
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
import uuid
from enum import Enum

class PresentationCameraFrameSearchSortByKey(str, Enum):
    TIMESTAMP_ASC = "timestamp_asc"
    TIMESTAMP_DESC = "timestamp_desc"

@dataclass
class PresentationCameraFrameSearchRequestBody(PresentationUtilRequestBody):
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    sort_by_list: list[PresentationCameraFrameSearchSortByKey] | None = None

class PresentationCameraFrameSearch(PresentationUtilBase):
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
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        body: PresentationCameraFrameSearchRequestBody | None = None,
        application: ApplicationCameraFrameSearch = get_application(ApplicationCameraFrameSearch),
    ) -> PresentationUtilJSONResponse:
        query = None
        if body is not None:
            query = DtoCameraFrameQuery(
                ids=body.ids,
                camera_ids=body.camera_ids,
                view_ids=body.view_ids,
                timestamp_after=body.timestamp_after,
                timestamp_before=body.timestamp_before,
                sort_by_list=[
                    DtoCameraFrameQuerySortByKey(sort_by.value)
                    for sort_by in body.sort_by_list
                ] if body.sort_by_list is not None else None,
            )
        camera_frames = application.search(query=query)
        return PresentationUtilJSONResponse(status=200, content={
            "camera_frames": [
                {
                    "id": str(camera_frame.id),
                    "camera_id": camera_frame.camera_id,
                    "view_id": camera_frame.view_id,
                    "timestamp": camera_frame.timestamp.isoformat(),
                } for camera_frame in camera_frames
            ]
        })
