from background import Background
from logger import Logger
from applications.person.snapshot.background.identify import ApplicationPersonSnapshotBackgroundIdentify
from environment import Environment

class BackgroundPersonSnapshotIdentify(Background):
    @property
    def name(self) -> str:
        return "person snapshot identify"

    def __init__(
        self,
        logger: Logger,
        application: ApplicationPersonSnapshotBackgroundIdentify,
    ):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotIdentify":
        return cls(
            logger=Logger("background_person_snapshot_identify"),
            application=ApplicationPersonSnapshotBackgroundIdentify.create(environment),
        )

    def handle(self, background_id: str) -> None:
        person_snapshot = self.application.identify()
        self.logger.background_info(
            background_id=background_id,
            name=self.name,
            message=f"person snapshot id: {person_snapshot.id}, identified as person id: {person_snapshot.person_id}",
        )
