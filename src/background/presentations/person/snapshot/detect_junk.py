from background.presentations.utils import BackgroundPresentationUtilsBase
from background.applications.person.snapshot.detect_junk import BackgroundApplicationPersonSnapshotDetectJunk
from environment import Environment
from logger import Logger

class BackgroundPersonSnapshotDetectJunk(BackgroundPresentationUtilsBase):
    def __init__(
        self,
        logger: Logger,
        application: BackgroundApplicationPersonSnapshotDetectJunk,
    ):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotDetectJunk":
        return cls(
            logger=Logger("background_person_snapshot_detect_junk"),
            application=BackgroundApplicationPersonSnapshotDetectJunk.create(environment),
        )

    @property
    def name(self) -> str:
        return "person_snapshot_detect_junk"

    def handle(self, process_id: str) -> None:
        id = self.application.detect_junk()
        self.logger.background_info(
            process_id=process_id,
            name=self.name,
            message=f"person snapshot detect junk: {id.id}",
        )
