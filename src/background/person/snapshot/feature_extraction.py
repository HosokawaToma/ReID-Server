from background import BackgroundJob, BackgroundJobError
from applications.person.snapshot.feature_extraction import ApplicationPersonSnapshotFeatureExtraction
from applications.person.snapshot.feature_extraction import ApplicationPersonSnapshotFeatureExtractionParams
from applications.person.snapshot.feature_extraction import ApplicationPersonSnapshotNotFoundError
from applications.person.snapshot.feature_extraction import ApplicationPersonSnapshotImageNotFoundError
from environment import Environment

from dataclasses import dataclass
import uuid

class BackgroundPersonSnapshotFeatureExtraction(BackgroundJob):
    @property
    def name(self) -> str:
        return "person_snapshot_feature_extraction"

    @property
    def id(self) -> uuid.UUID:
        return self.params.person_snapshot_id

    def __init__(
        self,
        application: ApplicationPersonSnapshotFeatureExtraction,
        params: ApplicationPersonSnapshotFeatureExtractionParams,
    ):
        self.application = application
        self.params = params

    async def execute(self) -> None:
        try:
            self.application.extract(
                ApplicationPersonSnapshotFeatureExtractionParams(
                    person_snapshot_id=self.params.person_snapshot_id,
                )
            )
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
            application=ApplicationPersonSnapshotFeatureExtraction.create(self.environment),
            params=ApplicationPersonSnapshotFeatureExtractionParams(
                person_snapshot_id=params.person_snapshot_id,
            ),
        )
