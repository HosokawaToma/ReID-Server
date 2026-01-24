from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearch
from dto.id import DtoId
from presentation import PresentationBase
from presentation import PresentationAdminClientAuthenticated
from presentation import PresentationRequest
from presentation import get_application
from logger import Logger
from presentation import PresentationImageResponse
import uuid


class PresentationPersonSnapshotImageSearch(PresentationBase):
    router_path = "/person/snapshot/image/search/{id}"
    methods = ["GET"]
    tags = ["Person Snapshot Image"]
    summary = "Search person snapshot image"
    description = "Search person snapshot image by image id"
    responses = {
        200: {
            "description": "Person snapshot image found",
        },
        404: {
            "description": "Person snapshot image not found",
        },
        500: {
            "description": "Internal server error",
        },
    }

    def __init__(
        self,
        logger: Logger,
    ):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotImageSearch":
        return cls(
            logger=Logger("presentation_person_snapshot_image_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationRequest,
        id: uuid.UUID,
        application: ApplicationPersonSnapshotImageSearch = get_application(ApplicationPersonSnapshotImageSearch),
    ):
        image = application.search(
            id=DtoId(id=id),
        )
        return PresentationImageResponse(status=200, image=image)
