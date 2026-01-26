from applications.person.snapshot.image.search.person_id import ApplicationPersonSnapshotImageSearchPersonId
from dto.id import DtoId
from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.request import PresentationUtilRequest
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.type import PresentationUtilPathUUID
from presentation.utils.factory import get_application
from logger import Logger


class PresentationPersonSnapshotImageSearchPersonId(PresentationUtilBase):
    router_path = "/person/snapshot/image/search/person_id/{person_id}"
    methods = ["GET"]
    tags = ["Person Snapshot Image"]
    summary = "Search person snapshot images by person id"
    description = "Search person snapshot images by person id"
    responses = {
        200: {
            "description": "Person snapshot images found",
        },
        404: {
            "description": "Person snapshot images not found",
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
    def create(cls) -> "PresentationPersonSnapshotImageSearchPersonId":
        return cls(
            logger=Logger("presentation_person_snapshot_image_search_person_id"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        request: PresentationUtilRequest,
        person_id: PresentationUtilPathUUID,
        application: ApplicationPersonSnapshotImageSearchPersonId = get_application(ApplicationPersonSnapshotImageSearchPersonId),
    ):
        image_ids = application.search(
            person_id=DtoId(id=person_id),
        )
        return PresentationUtilJSONResponse(
            status=200,
            content={
                "image_ids": [str(image_id) for image_id in image_ids],
            },
        )
