from background import BackgroundJob, BackgroundJobError
from applications.person.snapshot.identify import ApplicationPersonSnapshotIdentify
from applications.person.snapshot.identify import ApplicationPersonSnapshotIdentifyParams
from applications.person.snapshot.identify import ApplicationPersonSnapshotIdentifyError
from applications.person.snapshot.identify import ApplicationPersonSnapshotMissingFeatureError
from applications.person.snapshot.identify import ApplicationPersonSnapshotNotFoundError
from applications.person.snapshot.identify import ApplicationPersonSnapshotThresholdError
from environment import Environment

from dataclasses import dataclass
import uuid

class BackgroundPersonSnapshotIdentify(BackgroundJob):
    @property
    def name(self) -> str:
        return "person_snapshot_identify"

    @property
    def id(self) -> uuid.UUID:
        return self.params.person_snapshot_id

    def __init__(
        self,
        application: ApplicationPersonSnapshotIdentify,
        params: ApplicationPersonSnapshotIdentifyParams,
    ):
        self.application = application
        self.params = params

    async def execute(self) -> str:
        try:
            self.application.identify(self.params)
            return f"person snapshot id: {self.params.person_snapshot_id}"
        except ApplicationPersonSnapshotMissingFeatureError:
            raise BackgroundJobError(f"Person snapshot missing feature")
        except ApplicationPersonSnapshotNotFoundError:
            raise BackgroundJobError(f"Person snapshot not found")
        except ApplicationPersonSnapshotThresholdError:
            raise BackgroundJobError(f"No matching people found")
        except ApplicationPersonSnapshotIdentifyError:
            raise BackgroundJobError

@dataclass
class BackgroundPersonSnapshotIdentifyFactoryParams:
    person_snapshot_id: uuid.UUID

class BackgroundPersonSnapshotIdentifyFactory:
    def __init__(self, environment: Environment):
        self.environment = environment

    def create(self, params: BackgroundPersonSnapshotIdentifyFactoryParams) -> BackgroundPersonSnapshotIdentify:
        return BackgroundPersonSnapshotIdentify(
            application=ApplicationPersonSnapshotIdentify.create(self.environment),
            params=ApplicationPersonSnapshotIdentifyParams(
                person_snapshot_id=params.person_snapshot_id,
            ),
        )
