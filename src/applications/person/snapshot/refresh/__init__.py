"""
人物検出更新アプリケーション

クエリ条件に合う人物検出結果IDを再識別キューに投入する。
"""
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from applications import ApplicationBase
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from repositories.person.snapshot.reid_queue import RepositoryPersonSnapshotReidQueue


class ApplicationPersonSnapshotRefresh(ApplicationBase):
    """
    人物検出を更新（再識別キュー投入）するアプリケーションクラス。
    """

    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
        repository_person_snapshot_reid_queue: RepositoryPersonSnapshotReidQueue,
    ):
        """
        アプリケーションを初期化する。

        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        :param RepositoryPersonSnapshotReidQueue repository_person_snapshot_reid_queue: 再識別キュー
        """
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_person_snapshot_reid_queue = repository_person_snapshot_reid_queue

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotRefresh":
        """
        環境からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return ApplicationPersonSnapshotRefresh: アプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
            repository_person_snapshot_reid_queue=RepositoryPersonSnapshotReidQueue.create(
                environment),
        )

    def refresh(self, query: DtoPersonSnapshotQuery | None = None) -> None:
        """
        人物検出を更新する
        :param DtoPersonSnapshotQuery query: 人物検出更新条件
        :raises InternalServerError: 人物検出更新に失敗した場合に発生するエラー
        """
        database_query = None
        if query is not None:
            database_query = RepositoryUtilDatabaseQueryPersonSnapshot(
                ids=query.ids,
                camera_ids=query.camera_ids,
                view_ids=query.view_ids,
            )
        ids = self.repository_person_snapshot.find_ids(query=database_query)
        self.repository_person_snapshot_reid_queue.push_ids(ids)
