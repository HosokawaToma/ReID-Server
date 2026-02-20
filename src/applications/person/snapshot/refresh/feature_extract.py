"""
人物検出の特徴量再抽出アプリケーション

クエリ条件に合う人物検出結果IDを特徴量抽出キューに投入する。
"""
from applications import ApplicationBase
from repositories.person.snapshot.feature_extract_queue import RepositoryPersonSnapshotFeatureExtractQueue
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot


class ApplicationPersonSnapshotRefreshFeatureExtract(ApplicationBase):
    """
    人物検出の特徴量再抽出を担当するアプリケーション。

    クエリ条件に合う人物検出結果のIDを特徴量抽出キューに一括投入する。
    """

    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
        repository_person_snapshot_feature_extract_queue: RepositoryPersonSnapshotFeatureExtractQueue,
    ):
        """
        アプリケーションを初期化する。

        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        :param RepositoryPersonSnapshotFeatureExtractQueue repository_person_snapshot_feature_extract_queue: 特徴量抽出キュー
        """
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_person_snapshot_feature_extract_queue = repository_person_snapshot_feature_extract_queue

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotRefreshFeatureExtract":
        """
        環境からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return ApplicationPersonSnapshotRefreshFeatureExtract: アプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
            repository_person_snapshot_feature_extract_queue=RepositoryPersonSnapshotFeatureExtractQueue.create(
                environment),
        )

    def refresh(self, query: DtoPersonSnapshotQuery | None = None) -> None:
        """
        クエリ条件に合う人物検出結果のIDを特徴量抽出キューに投入する。条件が None の場合は該当する全IDを投入する。

        :param DtoPersonSnapshotQuery | None query: 対象とする人物検出の条件（省略時は全件）
        :raises InternalServerError: キュー投入などに失敗した場合
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
