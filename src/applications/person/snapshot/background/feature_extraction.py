from repositories.person.snapshot import RepositoryPersonSnapshot
from domain.person.snapshot import DomainPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotError
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtraction
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtractionError
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentify
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyQueueItem
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyError
from modules.reid.model import ModuleReIDModel
from environment import Environment
from error import Error


class ApplicationPersonSnapshotBackgroundFeatureExtractionError(Error):
    pass


class ApplicationPersonSnapshotBackgroundFeatureExtraction:
    def __init__(
        self,
        repository_queue_person_snapshot_feature_extraction: RepositoryQueuePersonSnapshotFeatureExtraction,
        repository_queue_person_snapshot_identify: RepositoryQueuePersonSnapshotIdentify,
        reid_model: ModuleReIDModel,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.repository_queue_person_snapshot_feature_extraction = repository_queue_person_snapshot_feature_extraction
        self.repository_queue_person_snapshot_identify = repository_queue_person_snapshot_identify
        self.reid_model = reid_model
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ApplicationPersonSnapshotBackgroundFeatureExtraction":
        return cls(
            repository_queue_person_snapshot_feature_extraction=RepositoryQueuePersonSnapshotFeatureExtraction.create(
                environment),
            repository_queue_person_snapshot_identify=RepositoryQueuePersonSnapshotIdentify.create(
                environment),
            reid_model=ModuleReIDModel(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def extract(self) -> DomainPersonSnapshot:
        try:
            queue_item = self.repository_queue_person_snapshot_feature_extraction.dequeue()
            person_snapshot = self.repository_person_snapshot.find_first(
                filters=RepositoryPersonSnapshotFilters(ids=[queue_item.id]))
            if person_snapshot is None:
                raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(
                    f"person snapshot not found: {queue_item.id}")
            person_snapshot.extract_feature(self.reid_model, self.repository_person_snapshot)
            self.repository_person_snapshot.update(person_snapshot)
            self.repository_queue_person_snapshot_identify.push(
                RepositoryQueuePersonSnapshotIdentifyQueueItem(id=person_snapshot.id))
            return person_snapshot
        except RepositoryQueuePersonSnapshotFeatureExtractionError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
        except RepositoryPersonSnapshotError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
        except RepositoryQueuePersonSnapshotIdentifyError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
