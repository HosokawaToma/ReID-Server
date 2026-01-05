from applications.frame.search import ApplicationFrameSearch
from environment import Environment
from presentation import PresentationBase
from logger import Logger
from presentation import PresentationRequestBody
from dto.frame_image.filter import DtoFrameImageFilter
from dto.frame_image.ordering import DtoFrameImageOrdering
from dataclasses import dataclass
from typing import Literal
from datetime import datetime
from presentation import PresentationJSONResponse
from presentation import PresentationAdminClientAuthenticated
import uuid

class PresentationFrameSearchFilters(PresentationRequestBody):
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

@dataclass
class PresentationFrameSearchRequestBody(PresentationRequestBody):
    filters: PresentationFrameSearchFilters | None = None
    ordering: list[Literal["timestamp_asc", "timestamp_desc"]] | None = None

class PresentationFrameSearch(PresentationBase):
    router_path = "/frame/search"
    methods = ["POST"]
    tags = ["Frame"]
    summary = "Search frames"
    description = "Search frames"
    responses = {
        200: {
            "description": "Frames",
        },
    }

    def __init__(self, logger: Logger, application: ApplicationFrameSearch):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "PresentationFrameSearch":
        return cls(
            logger=Logger("presentation_frame_search"),
            application=ApplicationFrameSearch.create(environment),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationFrameSearchRequestBody | None = None,
    ) -> PresentationJSONResponse:
        filters = None
        if request is not None and request.filters is not None:
            filters = DtoFrameImageFilter(
                ids=request.filters.ids,
                camera_ids=request.filters.camera_ids,
                view_ids=request.filters.view_ids,
                timestamp_after=request.filters.timestamp_after,
                timestamp_before=request.filters.timestamp_before,
            )
        ordering = None
        if request is not None and request.ordering is not None:
            ordering = DtoFrameImageOrdering(
                ordering=request.ordering,
            )
        frames = self.application.search(
            filters=filters,
            ordering=ordering,
        )
        return PresentationJSONResponse(status=200, content={
            "frames": [
                {
                    "id": str(frame.id),
                    "camera_id": frame.camera_id,
                    "view_id": frame.view_id,
                    "timestamp": frame.timestamp.isoformat(),
                } for frame in frames
            ]
        })
