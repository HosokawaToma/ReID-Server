from applications.person.snapshot.create import ApplicationPersonSnapshotCreate
from applications.person.snapshot.create import ApplicationPersonSnapshotCreateParams
from presentation import PresentationBase
from presentation import PresentationAdminClientAuthenticated
from presentation import PresentationTypeImage
from presentation import PresentationTypeDatetime
from presentation import PresentationTypeInt
from presentation import PresentationJSONResponse
from logger import Logger
from environment import Environment

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
        application: ApplicationPersonSnapshotCreate,
    ):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "PresentationPersonSnapshotCreate":
        return cls(
            logger=Logger("presentation_person_snapshot_create"),
            application=ApplicationPersonSnapshotCreate.create(
                environment=environment,
            ),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        image: PresentationTypeImage,
        timestamp: PresentationTypeDatetime,
        camera_id: PresentationTypeInt,
        view_id: PresentationTypeInt,
    ):
        self.application.save(
            ApplicationPersonSnapshotCreateParams(
                image=image,
                timestamp=timestamp,
                camera_id=camera_id,
                view_id=view_id,
            ),
        )
        return PresentationJSONResponse(status=200, content={"message": "Person snapshot created"})
