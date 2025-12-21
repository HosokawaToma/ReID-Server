from background import Background
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotBackgroundFeatureExtraction
from environment import Environment
from logger import Logger

class BackgroundPersonSnapshotFeatureExtraction(Background):
    def __init__(
        self,
        logger: Logger,
        application: ApplicationPersonSnapshotBackgroundFeatureExtraction,
    ):
        super().__init__(logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotFeatureExtraction":
        return cls(
            application=ApplicationPersonSnapshotBackgroundFeatureExtraction.create(environment),
            logger=Logger("person_snapshot_feature_extraction"),
        )

    @property
    def name(self) -> str:
        return "person_snapshot_feature_extraction"

    def handle(self) -> str:
        person_snapshot = self.application.extract()
        return f"feature extracted for person snapshot id: {person_snapshot.id}"
