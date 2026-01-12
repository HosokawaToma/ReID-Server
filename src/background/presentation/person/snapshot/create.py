from background.presentation.utils import BackgroundPresentationUtilsBase
from logger import Logger
from applications.person.snapshot.background.create import ApplicationPersonSnapshotBackgroundCreate
from environment import Environment

class BackgroundPersonSnapshotCreate(BackgroundPresentationUtilsBase):
    @property
    def name(self) -> str:
        return "person snapshot create"

    def __init__(
        self,
        logger: Logger,
        application: ApplicationPersonSnapshotBackgroundCreate,
    ):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotCreate":
        return cls(
            logger=Logger("background_person_snapshot_create"),
            application=ApplicationPersonSnapshotBackgroundCreate.create(environment),
        )

    def handle(self, background_id: str) -> None:
        meta_data = self.application.save()
        self.logger.background_info(
            background_id=background_id,
            name=self.name,
            message=f"frame image id: {meta_data.id} created",
        )
