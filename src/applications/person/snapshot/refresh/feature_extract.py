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
        """
        人物検出結果の特徴量を再抽出する
        :param DtoPersonSnapshotQuery query: 人物検出結果の特徴量を再抽出する条件
        :raises InternalServerError: 人物検出結果の特徴量を再抽出に失敗した場合に発生するエラー
        """
        database_query = None
        if query is not None:
            database_query = RepositoryUtilDatabaseQueryPersonSnapshot(
                ids=query.ids,
                person_ids=query.person_ids,
                camera_ids=query.camera_ids,
                view_ids=query.view_ids,
                is_junk=query.is_junk,
                timestamp_after=query.timestamp_after,
                timestamp_before=query.timestamp_before,
            )
        ids = self.repository_person_snapshot.find_ids(query=database_query)
        self.repository_person_snapshot_feature_extract_queue.push_ids(ids)
