from applications.person.snapshot.create import ApplicationPersonSnapshotCreate
from dto.location import DtoLocation
from dto.timestamp import DtoTimestamp
from presentation.utils.base import PresentationUtilBase
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.type import PresentationUtilFromImage, PresentationUtilFromDatetime, PresentationUtilFromInt
from presentation.utils.response import PresentationUtilJSONResponse
from logger import Logger
from presentation.utils.factory import get_application


class PresentationPersonSnapshotCreate(PresentationUtilBase):
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
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        image: PresentationUtilFromImage,
        timestamp: PresentationUtilFromDatetime,
        camera_id: PresentationUtilFromInt,
        view_id: PresentationUtilFromInt,
        application: ApplicationPersonSnapshotCreate = get_application(ApplicationPersonSnapshotCreate),
    ):
        application.save(
            location=DtoLocation(camera_id=camera_id, view_id=view_id),
            timestamp=DtoTimestamp(timestamp=timestamp),
            image=image,
        )
        return PresentationUtilJSONResponse(status=200, content={"message": "Person snapshot created"})
