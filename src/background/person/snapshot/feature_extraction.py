from background import Background, BackgroundJobError, BackgroundLogger
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotBackgroundFeatureExtraction
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotNotFoundError
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotImageNotFoundError
from environment import Environment

class BackgroundPersonSnapshotFeatureExtraction(Background):
    def __init__(
        self,
        application: ApplicationPersonSnapshotBackgroundFeatureExtraction,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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

    async def process(self) -> None:
        try:
            await self.application.extract()
        except ApplicationPersonSnapshotNotFoundError:
            raise BackgroundJobError("person snapshot not found")
        except ApplicationPersonSnapshotImageNotFoundError:
            raise BackgroundJobError("person snapshot image not found")
