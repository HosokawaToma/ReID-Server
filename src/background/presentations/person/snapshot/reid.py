from background.presentations.utils import BackgroundPresentationUtilsBase
from background.applications.person.snapshot.reid import BackgroundApplicationPersonSnapshotReid
from environment import Environment
from logger import Logger

class BackgroundPersonSnapshotReid(BackgroundPresentationUtilsBase):
    def __init__(
        self,
        logger: Logger,
        application: BackgroundApplicationPersonSnapshotReid,
    ):
        super().__init__(logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotReid":
        return cls(
            application=BackgroundApplicationPersonSnapshotReid.create(environment),
            logger=Logger("background_person_snapshot_reid"),
        )

    @property
    def name(self) -> str:
        return "person_snapshot_reid"

    def handle(self, process_id: str) -> None:
        person_snapshot_person_id = self.application.reid()
        self.logger.background_info(
            process_id=process_id,
            name=self.name,
            message=f"person snapshot id: {person_snapshot_person_id.id} reid",
        )
