from background import BackgroundJob, BackgroundJobError
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotBackgroundFeatureExtraction
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotNotFoundError
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotImageNotFoundError
from environment import Environment

from dataclasses import dataclass
import uuid

class BackgroundPersonSnapshotFeatureExtraction(BackgroundJob):
    @property
    def name(self) -> str:
        return "person_snapshot_feature_extraction"

    def __init__(
        self,
        application: ApplicationPersonSnapshotBackgroundFeatureExtraction,
    ):
        self.application = application

    async def execute(self) -> str:
        try:
            return await self.application.extract()
        except ApplicationPersonSnapshotNotFoundError:
            raise BackgroundJobError("person snapshot not found")
        except ApplicationPersonSnapshotImageNotFoundError:
            raise BackgroundJobError("person snapshot image not found")

@dataclass
class BackgroundPersonSnapshotFeatureExtractionFactoryParams:
    person_snapshot_id: uuid.UUID

class BackgroundPersonSnapshotFeatureExtractionFactory:
    def __init__(self, environment: Environment):
        self.environment = environment

    def create(self, params: BackgroundPersonSnapshotFeatureExtractionFactoryParams) -> BackgroundPersonSnapshotFeatureExtraction:
        return BackgroundPersonSnapshotFeatureExtraction(
            application=ApplicationPersonSnapshotBackgroundFeatureExtraction.create(self.environment),
        )
