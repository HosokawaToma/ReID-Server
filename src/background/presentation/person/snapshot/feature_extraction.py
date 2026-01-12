from background.presentation.utils import BackgroundPresentationUtilsBase
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotBackgroundFeatureExtraction
from environment import Environment
from logger import Logger

class BackgroundPersonSnapshotFeatureExtraction(BackgroundPresentationUtilsBase):
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
            logger=Logger("background_person_snapshot_feature_extraction"),
        )

    @property
    def name(self) -> str:
        return "person snapshot feature extraction"

    def handle(self, background_id: str) -> None:
        person_snapshot = self.application.extract()
        self.logger.background_info(
            background_id=background_id,
            name=self.name,
            message=f"person snapshot id: {person_snapshot.id} extracted",
        )
