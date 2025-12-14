from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotOrdering
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
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
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

    def refresh(self, params: ApplicationPersonSnapshotRefreshParams) -> None:
        try:
            person_snapshots = self.repository_person_snapshot.find(
                filters=RepositoryPersonSnapshotFilters(
                    timestamp_after=params.timestamp_after,
                    timestamp_before=params.timestamp_before,
                    camera_ids=params.camera_ids,
                    view_ids=params.view_ids,
                ),
                ordering=RepositoryPersonSnapshotOrdering(
                    ordering=[RepositoryPersonSnapshotOrdering.KEY_TIMESTAMP_ASC],
                ),
            )
            queue_items = person_snapshots.to_feature_extraction_queue_items()
            for queue_item in queue_items:
                self.repository_queue_person_snapshot_feature_extraction.push(queue_item)
        except RepositoryQueuePersonSnapshotFeatureExtractionError as e:
            raise ApplicationPersonSnapshotFeatureExtractionQueueError(e.message)
        except RepositoryQueuePersonSnapshotIdentifyError as e:
            raise ApplicationPersonSnapshotIdentifyQueueError(e.message)
