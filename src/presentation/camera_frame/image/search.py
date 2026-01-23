from applications.camera_frame.image.search import ApplicationCameraFrameImageSearch
from presentation import PresentationBase, get_application
from presentation import PresentationAdminClientAuthenticated
from presentation import PresentationImageResponse
from presentation import PresentationRequest
from logger import Logger
import uuid
from dto.id import DtoId

class PresentationCameraFrameImageSearch(PresentationBase):
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
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationRequest,
        id: uuid.UUID,
        application: ApplicationCameraFrameImageSearch = get_application(ApplicationCameraFrameImageSearch),
    ) -> PresentationImageResponse:
        image = application.search(
            id=DtoId(id=id),
        )
        return PresentationImageResponse(status=200, image=image.image)
