from background.presentation.utils import BackgroundPresentationUtilsBase
from logger import Logger
from background.application.person.snapshot.identify import BackgroundApplicationPersonSnapshotIdentify
from environment import Environment

class BackgroundPersonSnapshotIdentify(BackgroundPresentationUtilsBase):
    @property
    def name(self) -> str:
        return "person snapshot identify"

    def __init__(
        self,
        logger: Logger,
        application: BackgroundApplicationPersonSnapshotIdentify,
    ):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotIdentify":
        return cls(
            logger=Logger("background_person_snapshot_identify"),
            application=BackgroundApplicationPersonSnapshotIdentify.create(environment),
        )

    def handle(self, background_id: str) -> None:
        person_snapshot = self.application.identify()
        self.logger.background_info(
            background_id=background_id,
            name=self.name,
            message=f"person snapshot id: {person_snapshot.id}, identified as person id: {person_snapshot.person_id}",
        )
