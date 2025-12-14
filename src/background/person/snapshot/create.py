from background import Background
from background import BackgroundLogger
from applications.person.snapshot.background.create import ApplicationPersonSnapshotBackgroundCreate
from environment import Environment

class BackgroundPersonSnapshotCreate(Background):
    @property
    def name(self) -> str:
        return "person snapshot create"

    def __init__(
        self,
        logger: BackgroundLogger,
        application: ApplicationPersonSnapshotBackgroundCreate,
    ):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotCreate":
        return cls(
            logger=BackgroundLogger(),
            application=ApplicationPersonSnapshotBackgroundCreate.create(environment),
        )
    def handle(self) -> str:
        self.application.save()
        return "person snapshot created"
