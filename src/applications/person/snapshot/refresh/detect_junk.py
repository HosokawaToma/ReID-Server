"""
人物検出のジャンク再判定アプリケーション

クエリ条件に合う人物検出結果IDをジャンク判定キューに投入する。
"""
from applications import ApplicationBase
from repositories.person.snapshot.detect_junk_queue import RepositoryPersonSnapshotDetectJunkQueue
from environment import Environment
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshot


class ApplicationPersonSnapshotRefreshDetectJunk(ApplicationBase):
    """
    人物検出のジャンク再判定を担当するアプリケーション。

    クエリ条件に合う人物検出結果のIDをジャンク判定キューに一括投入する。
    """

    def __init__(
        self,
        repository_person_snapshot_detect_junk_queue: RepositoryPersonSnapshotDetectJunkQueue,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        """
        アプリケーションを初期化する。

        :param RepositoryPersonSnapshotDetectJunkQueue repository_person_snapshot_detect_junk_queue: ジャンク判定キュー
        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        """
        self.repository_person_snapshot_detect_junk_queue = repository_person_snapshot_detect_junk_queue
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotRefreshDetectJunk":
        """
        環境変数からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境変数
        :return ApplicationPersonSnapshotRefreshDetectJunk: アプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot_detect_junk_queue=RepositoryPersonSnapshotDetectJunkQueue.create(
                environment),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def refresh(self, query: DtoPersonSnapshotQuery | None = None) -> None:
        """
        クエリ条件に合う人物検出結果のIDをジャンク判定キューに投入する。条件が None の場合は該当する全IDを投入する。

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
        self.repository_person_snapshot_detect_junk_queue.push_ids(ids)
