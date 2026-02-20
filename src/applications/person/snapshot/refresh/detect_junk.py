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
    人物検出結果のジャンクを再判定するアプリケーションクラス。

    条件に合うIDをジャンク判定キューに push する。
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
        環境からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
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
                is_junk=query.is_junk,
                timestamp_after=query.timestamp_after,
                timestamp_before=query.timestamp_before,
            )
        ids = self.repository_person_snapshot.find_ids(query=database_query)
        self.repository_person_snapshot_detect_junk_queue.push_ids(ids)
