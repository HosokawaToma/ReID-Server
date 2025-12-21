from background import Background
from logger import Logger
from applications.person.snapshot.background.create import ApplicationPersonSnapshotBackgroundCreate
from environment import Environment

class BackgroundPersonSnapshotCreate(Background):
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
            logger=Logger("person_snapshot_create"),
            application=ApplicationPersonSnapshotBackgroundCreate.create(environment),
        )
    def handle(self) -> str:
        self.application.save()
        return "person snapshot created"
