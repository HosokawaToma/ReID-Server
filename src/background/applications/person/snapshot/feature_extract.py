from repositories.person.snapshot.feature_extract_queue import RepositoryPersonSnapshotFeatureExtractQueue
from repositories.reid import RepositoryReID
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from background.applications.utils import BackgroundApplicationUtilsBase

class BackgroundApplicationPersonSnapshotFeatureExtract(BackgroundApplicationUtilsBase):
    def __init__(
        self,
        repository_person_snapshot_feature_extract_queue: RepositoryPersonSnapshotFeatureExtractQueue,
        repository_reid: RepositoryReID,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.repository_person_snapshot_feature_extract_queue = repository_person_snapshot_feature_extract_queue
        self.repository_reid = repository_reid
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundApplicationPersonSnapshotFeatureExtract":
        return cls(
            repository_person_snapshot_feature_extract_queue=RepositoryPersonSnapshotFeatureExtractQueue.create(environment),
            repository_reid=RepositoryReID.create(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
        )

    def extract(self) -> None:
        person_snapshot_image = self.repository_person_snapshot_feature_extract_queue.pop()
        feature = person_snapshot_image.extract_feature(reid_model=self.repository_reid.find())
        self.repository_person_snapshot.save_feature(feature)
