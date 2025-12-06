from background import Background, BackgroundJobError, BackgroundLogger
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotBackgroundFeatureExtraction
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotBackgroundFeatureExtractionError
from environment import Environment

class BackgroundPersonSnapshotFeatureExtraction(Background):
    def __init__(
        self,
        logger: BackgroundLogger,
        application: ApplicationPersonSnapshotBackgroundFeatureExtraction,
    ):
        super().__init__(logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotFeatureExtraction":
        return cls(
            application=ApplicationPersonSnapshotBackgroundFeatureExtraction.create(environment),
            logger=BackgroundLogger(),
        )

    @property
    def name(self) -> str:
        return "person_snapshot_feature_extraction"

    async def process(self) -> str:
        try:
            person_snapshot = await self.application.extract()
            return f"feature extracted for person snapshot id: {person_snapshot.id}"
        except ApplicationPersonSnapshotBackgroundFeatureExtractionError as e:
            raise BackgroundJobError(e.message)
