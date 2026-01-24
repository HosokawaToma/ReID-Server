from background.presentations.utils import BackgroundPresentationUtilsBase
from logger import Logger
from background.applications.person.snapshot.create import BackgroundApplicationPersonSnapshotCreate
from environment import Environment

class BackgroundPersonSnapshotCreate(BackgroundPresentationUtilsBase):
    def __init__(
        self,
        logger: Logger,
        application: BackgroundApplicationPersonSnapshotCreate,
    ):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotCreate":
        return cls(
            logger=Logger("background_person_snapshot_create"),
            application=BackgroundApplicationPersonSnapshotCreate.create(environment),
        )

    @property
    def name(self) -> str:
        return "person_snapshot_create"

    def handle(self, process_id: str) -> None:
        self.application.save()
        self.logger.background_info(
            process_id=process_id,
            name=self.name,
            message=f"person snapshot created",
        )
