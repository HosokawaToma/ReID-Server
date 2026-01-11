from applications.frame.image.search import ApplicationFrameImageSearch
from presentation import PresentationBase, get_application
from presentation import PresentationAdminClientAuthenticated
from presentation import PresentationImageResponse
from presentation import PresentationRequest
from logger import Logger
import uuid

class PresentationFrameImageSearch(PresentationBase):
    router_path = "/frame/image/search/{id}"
    methods = ["GET"]
    tags = ["Frame Image"]
    summary = "Search frame images"
    description = "Search frame images"
    responses = {
        200: {
            "description": "Frame images",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationFrameImageSearch":
        return cls(
            logger=Logger("presentation_frame_image_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationRequest,
        id: uuid.UUID,
        application: ApplicationFrameImageSearch = get_application(ApplicationFrameImageSearch),
    ) -> PresentationImageResponse:
        image = application.search(
            id=id,
        )
        return PresentationImageResponse(status=200, image=image.image)
