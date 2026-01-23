from applications.person.snapshot.create import ApplicationPersonSnapshotCreate
from dto.image import DtoImage
from dto.location import DtoLocation
from dto.timestamp import DtoTimestamp
from presentation import PresentationBase
from presentation import PresentationAdminClientAuthenticated
from presentation import PresentationTypeImage
from presentation import PresentationTypeDatetime
from presentation import PresentationTypeInt
from presentation import PresentationJSONResponse
from logger import Logger
from presentation import get_application


class PresentationPersonSnapshotCreate(PresentationBase):
    router_path = "/person/snapshot/create"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Create a person snapshot"
    description = "Create a person snapshot"
    responses = {
        200: {"description": "Person snapshot created"},
        400: {"description": "Bad request"},
    }

    def __init__(
        self,
        logger: Logger,
    ):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotCreate":
        return cls(
            logger=Logger("presentation_person_snapshot_create"),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        image: PresentationTypeImage,
        timestamp: PresentationTypeDatetime,
        camera_id: PresentationTypeInt,
        view_id: PresentationTypeInt,
        application: ApplicationPersonSnapshotCreate = get_application(ApplicationPersonSnapshotCreate),
    ):
        if image.format is None:
            return PresentationJSONResponse(status=400, content={"message": "Image format is None"})
        application.save(
            location=DtoLocation(camera_id=camera_id, view_id=view_id),
            timestamp=DtoTimestamp(timestamp=timestamp),
            image=DtoImage(image=image, format=image.format),
        )
        return PresentationJSONResponse(status=200, content={"message": "Person snapshot created"})
