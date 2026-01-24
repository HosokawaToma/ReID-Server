from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearch
from dto.id import DtoId
from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.request import PresentationUtilRequest
from presentation.utils.response import PresentationUtilImageResponse
from presentation.utils.type import PresentationUtilPathUUID
from logger import Logger


class PresentationPersonSnapshotImageSearch(PresentationUtilBase):
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
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationUtilRequest,
        id: PresentationUtilPathUUID,
        application: ApplicationPersonSnapshotImageSearch = get_application(ApplicationPersonSnapshotImageSearch),
    ):
        image = application.search(
            id=DtoId(id=id),
        )
        return PresentationUtilImageResponse(status=200, image=image)
