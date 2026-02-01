from applications import ApplicationBase
from repositories.person.snapshot.detect_junk_queue import RepositoryPersonSnapshotDetectJunkQueue
from environment import Environment
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshot

class ApplicationPersonSnapshotRefreshDetectJunk(ApplicationBase):
    def __init__(
        self,
        repository_person_snapshot_detect_junk_queue: RepositoryPersonSnapshotDetectJunkQueue,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.repository_person_snapshot_detect_junk_queue = repository_person_snapshot_detect_junk_queue
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotRefreshDetectJunk":
        return cls(
            repository_person_snapshot_detect_junk_queue=RepositoryPersonSnapshotDetectJunkQueue.create(environment),
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
        )

    def refresh(self, query: DtoPersonSnapshotQuery | None = None) -> None:
        """
        人物検出結果のゴミデータを再判定する
        :param DtoPersonSnapshotQuery query: 人物検出結果のゴミデータを再判定する条件
        :raises InternalServerError: 人物検出結果のゴミデータを再判定に失敗した場合に発生するエラー
        """
        database_query = None
        if query is not None:
            database_query = RepositoryUtilDatabaseQueryPersonSnapshot(
                ids=query.ids,
                person_ids=query.person_ids,
                camera_ids=query.camera_ids,
                view_ids=query.view_ids,
            )
        ids = self.repository_person_snapshot.find_ids(query=database_query)
        self.repository_person_snapshot_detect_junk_queue.push_ids(ids)
