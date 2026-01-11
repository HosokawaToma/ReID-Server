from applications.person.snapshot.create import ApplicationPersonSnapshotCreate
from dto.image import DtoImage
from dto.frame_image.property import DtoFrameImageProperty
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
        application.save(
            image=DtoImage(
                image=image,
            ),
            frame_image_property=DtoFrameImageProperty(
                camera_id=camera_id,
                view_id=view_id,
                timestamp=timestamp,
            ),
        )
        return PresentationJSONResponse(status=200, content={"message": "Person snapshot created"})
