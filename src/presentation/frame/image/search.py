from applications.frame.image.search import ApplicationFrameImageSearch
from environment import Environment
from presentation import PresentationBase
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

    def __init__(self, logger: Logger, application: ApplicationFrameImageSearch):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "PresentationFrameImageSearch":
        return cls(
            logger=Logger("presentation_frame_image_search"),
            application=ApplicationFrameImageSearch.create(environment),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationRequest,
        id: uuid.UUID,
    ) -> PresentationImageResponse:
        image = self.application.search(
            id=id,
        )
        return PresentationImageResponse(status=200, image=image.image)
