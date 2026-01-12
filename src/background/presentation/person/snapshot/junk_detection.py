from background.presentation.utils import BackgroundPresentationUtilsBase
from applications.person.snapshot.background.junk_detection import ApplicationPersonSnapshotBackgroundJunkDetection
from logger import Logger
from environment import Environment

class BackgroundPersonSnapshotJunkDetection(BackgroundPresentationUtilsBase):
    @property
    def name(self) -> str:
        return "person snapshot junk detection"

    def __init__(self, logger: Logger, application: ApplicationPersonSnapshotBackgroundJunkDetection):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotJunkDetection":
        return cls(
            logger=Logger("background_person_snapshot_junk_detection"),
            application=ApplicationPersonSnapshotBackgroundJunkDetection.create(environment),
        )

    def handle(self, background_id: str) -> None:
        person_snapshot = self.application.detect()
        if person_snapshot.is_junk:
            self.logger.background_info(
                background_id=background_id,
                name=self.name,
                message=f"person snapshot id: {person_snapshot.id} detected as junk",
            )
        else:
            self.logger.background_info(
                background_id=background_id,
                name=self.name,
                message=f"person snapshot id: {person_snapshot.id} detected as not junk",
            )
