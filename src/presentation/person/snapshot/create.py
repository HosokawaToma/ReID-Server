from applications.person.snapshot.create import ApplicationPersonSnapshotCreate
from applications.person.snapshot.create import ApplicationPersonSnapshotCreateParams
from presentation import PresentationBase
from presentation import PresentationTypeAuthorization
from presentation import PresentationTypeImage
from presentation import PresentationTypeDatetime
from applications.auth.camera_client import ApplicationAuthCameraClient
from presentation import PresentationJSONResponse

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
        auth: ApplicationAuthCameraClient,
        application: ApplicationPersonSnapshotCreate,
    ):
        self.auth = auth
        self.application = application

    async def handle(
        self,
        authorization: PresentationTypeAuthorization,
        image: PresentationTypeImage,
        timestamp: PresentationTypeDatetime,
    ):
        jwt = self.auth.verify(authorization)
        self.application.save(
            ApplicationPersonSnapshotCreateParams(
                image=image,
                timestamp=timestamp,
                camera_id=jwt.camera_id,
                view_id=jwt.view_id,
            ),
        )
        return PresentationJSONResponse(status=200, content={"message": "Person snapshot created"})
