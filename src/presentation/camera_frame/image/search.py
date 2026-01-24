from applications.camera_frame.image.search import ApplicationCameraFrameImageSearch
from presentation.utils.base import PresentationUtilBase
from presentation.utils.factory import get_application
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.response import PresentationUtilImageResponse
from presentation.utils.request import PresentationUtilRequest
from presentation.utils.type import PresentationUtilPathUUID
from logger import Logger
from dto.id import DtoId

class PresentationCameraFrameImageSearch(PresentationUtilBase):
    router_path = "/camera_frame/image/search/{id}"
    methods = ["GET"]
    tags = ["Camera Frame Image"]
    summary = "Search camera frame images"
    description = "Search camera frame images"
    responses = {
        200: {
            "description": "Camera frame images",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationCameraFrameImageSearch":
        return cls(
            logger=Logger("presentation_camera_frame_image_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationUtilRequest,
        id: PresentationUtilPathUUID,
        application: ApplicationCameraFrameImageSearch = get_application(ApplicationCameraFrameImageSearch),
    ) -> PresentationUtilImageResponse:
        image = application.search(
            id=DtoId(id=id),
        )
        return PresentationUtilImageResponse(status=200, image=image)
