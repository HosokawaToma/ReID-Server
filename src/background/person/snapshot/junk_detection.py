from background import Background
from applications.person.snapshot.background.junk_detection import ApplicationPersonSnapshotBackgroundJunkDetection
from logger import Logger
from environment import Environment

class BackgroundPersonSnapshotJunkDetection(Background):
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

    def handle(self) -> str:
        person_snapshot = self.application.detect()
        if person_snapshot.is_junk:
            return f"person snapshot id: {person_snapshot.id} detected as junk"
        else:
            return f"person snapshot id: {person_snapshot.id} detected as not junk"
