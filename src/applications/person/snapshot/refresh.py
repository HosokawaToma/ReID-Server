from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from error import Error
from applications import ApplicationBase
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from repositories.person.snapshot.reid_queue import RepositoryPersonSnapshotReidQueue

class ApplicationPersonSnapshotRefreshError(Error):
    pass

class ApplicationPersonSnapshotRefresh(ApplicationBase):
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
        repository_person_snapshot_reid_queue: RepositoryPersonSnapshotReidQueue,
    ):
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_person_snapshot_reid_queue = repository_person_snapshot_reid_queue

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotRefresh":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
            repository_person_snapshot_reid_queue=RepositoryPersonSnapshotReidQueue.create(environment),
        )

    def refresh(self, query: DtoPersonSnapshotQuery | None = None) -> None:
        try:
            database_query = None
            if query is not None:
                database_query = RepositoryUtilDatabaseQueryPersonSnapshot(
                    ids=query.ids,
                    camera_ids=query.camera_ids,
                    view_ids=query.view_ids,
                )
            ids = self.repository_person_snapshot.find_ids(query=database_query)
            self.repository_person_snapshot_reid_queue.push_ids(ids)
        except Error as error:
            raise ApplicationPersonSnapshotRefreshError(error) from error
