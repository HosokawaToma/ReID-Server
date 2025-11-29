from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFindParams
from repositories.person.snapshot import RepositoryPersonSnapshotFindFilters
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtraction
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtractionQueueItem
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtractionError
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentify
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyQueueItem
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyError
from environment import Environment
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ApplicationPersonSnapshotRefreshParams:
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None

class ApplicationPersonSnapshotRefreshError(Exception):
    pass

class ApplicationPersonSnapshotFeatureExtractionQueueError(ApplicationPersonSnapshotRefreshError):
    pass

class ApplicationPersonSnapshotIdentifyQueueError(ApplicationPersonSnapshotRefreshError):
    pass

class ApplicationPersonSnapshotRefresh:
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
        repository_queue_person_snapshot_feature_extraction: RepositoryQueuePersonSnapshotFeatureExtraction,
        repository_queue_person_snapshot_identify: RepositoryQueuePersonSnapshotIdentify,
    ):
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_queue_person_snapshot_feature_extraction = repository_queue_person_snapshot_feature_extraction
        self.repository_queue_person_snapshot_identify = repository_queue_person_snapshot_identify

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotRefresh":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
            repository_queue_person_snapshot_feature_extraction=RepositoryQueuePersonSnapshotFeatureExtraction.create(environment),
            repository_queue_person_snapshot_identify=RepositoryQueuePersonSnapshotIdentify.create(environment),
        )

    async def refresh(self, params: ApplicationPersonSnapshotRefreshParams) -> None:
        try:
            person_snapshots = self.repository_person_snapshot.find(RepositoryPersonSnapshotFindParams(
                filters=RepositoryPersonSnapshotFindFilters(
                    after_timestamp=params.after_timestamp,
                    before_timestamp=params.before_timestamp,
                    camera_ids=params.camera_ids,
                    view_ids=params.view_ids,
                ),
            ))
            for person_snapshot in person_snapshots:
                await self.repository_queue_person_snapshot_feature_extraction.push(
                    RepositoryQueuePersonSnapshotFeatureExtractionQueueItem(
                        id=person_snapshot.id,
                    )
                )
                await self.repository_queue_person_snapshot_identify.push(
                    RepositoryQueuePersonSnapshotIdentifyQueueItem(
                        id=person_snapshot.id,
                    )
                )
        except RepositoryQueuePersonSnapshotFeatureExtractionError:
            raise ApplicationPersonSnapshotFeatureExtractionQueueError
        except RepositoryQueuePersonSnapshotIdentifyError:
            raise ApplicationPersonSnapshotIdentifyQueueError
