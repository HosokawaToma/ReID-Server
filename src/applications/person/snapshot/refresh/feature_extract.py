from applications import ApplicationBase
from repositories.person.snapshot.feature_extract_queue import RepositoryPersonSnapshotFeatureExtractQueue
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot

class ApplicationPersonSnapshotRefreshFeatureExtract(ApplicationBase):
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
        repository_person_snapshot_feature_extract_queue: RepositoryPersonSnapshotFeatureExtractQueue,
    ):
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_person_snapshot_feature_extract_queue = repository_person_snapshot_feature_extract_queue

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotRefreshFeatureExtract":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
            repository_person_snapshot_feature_extract_queue=RepositoryPersonSnapshotFeatureExtractQueue.create(environment),
        )

    def refresh(self, query: DtoPersonSnapshotQuery | None = None) -> None:
        database_query = None
        if query is not None:
            database_query = RepositoryUtilDatabaseQueryPersonSnapshot(
                ids=query.ids,
                camera_ids=query.camera_ids,
                view_ids=query.view_ids,
            )
        ids = self.repository_person_snapshot.find_ids(query=database_query)
        self.repository_person_snapshot_feature_extract_queue.push_ids(ids)
