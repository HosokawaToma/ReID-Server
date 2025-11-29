from applications.person.snapshot.create import ApplicationPersonSnapshotCreate
from applications.person.snapshot.create import ApplicationPersonSnapshotCreateParams
from presentation import PresentationBase
from presentation import PresentationTypeAuthorization
from presentation import PresentationTypeImage
from presentation import PresentationTypeDatetime
from applications.auth.camera_client import ApplicationAuthCameraClient
from background import BackgroundQueue
from background.person.snapshot.feature_extraction import BackgroundPersonSnapshotFeatureExtractionFactory
from background.person.snapshot.feature_extraction import BackgroundPersonSnapshotFeatureExtractionFactoryParams
from background.person.snapshot.identify import BackgroundPersonSnapshotIdentifyFactory
from background.person.snapshot.identify import BackgroundPersonSnapshotIdentifyFactoryParams

class PresentationPersonSnapshotCreate(PresentationBase):
    @property
    def router_path(self) -> str:
        return "/person/snapshot/create"

    @property
    def methods(self) -> list[str]:
        return ["POST"]

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
        background_queue: BackgroundQueue,
        background_person_snapshot_feature_extraction_factory: BackgroundPersonSnapshotFeatureExtractionFactory,
        background_person_snapshot_identify_factory: BackgroundPersonSnapshotIdentifyFactory,
    ):
        self.auth = auth
        self.application = application
        self.background_queue = background_queue
        self.background_person_snapshot_feature_extraction_factory = background_person_snapshot_feature_extraction_factory
        self.background_person_snapshot_identify_factory = background_person_snapshot_identify_factory

    async def handle(
        self,
        authorization: PresentationTypeAuthorization,
        image: PresentationTypeImage,
        timestamp: PresentationTypeDatetime,
    ) -> None:
        jwt = self.auth.verify(authorization)
        person_snapshot = self.application.save(ApplicationPersonSnapshotCreateParams(
            image=image,
            timestamp=timestamp,
            camera_id=jwt.camera_id,
            view_id=jwt.view_id,
        ))
        await self.background_queue.put(
            self.background_person_snapshot_feature_extraction_factory.create(
                params=BackgroundPersonSnapshotFeatureExtractionFactoryParams(
                    person_snapshot_id=person_snapshot.id,
                ),
            ),
        )
        await self.background_queue.put(
            self.background_person_snapshot_identify_factory.create(
                params=BackgroundPersonSnapshotIdentifyFactoryParams(
                    person_snapshot_id=person_snapshot.id,
                ),
            ),
        )
