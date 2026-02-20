"""
人物検出再識別のバックグラウンドアプリケーション

キューから1件取り出し、最近傍と照合して person_id を決定し、保存してDTOを返す。
"""
from repositories.person.snapshot.reid_queue import RepositoryPersonSnapshotReidQueue
from domain.reid.model import DomainReIDModel
from modules.reid.model import ModuleReIDModel
from environment import Environment
from background.applications.utils import BackgroundApplicationUtilsBase
from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.person.snapshot.person_id import DtoPersonSnapshotPersonId


class BackgroundApplicationPersonSnapshotReid(BackgroundApplicationUtilsBase):
    """
    人物検出を1件再識別するバックグラウンドアプリケーションクラス。
    """

    def __init__(
        self,
        repository_person_snapshot_reid_queue: RepositoryPersonSnapshotReidQueue,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        """
        バックグラウンドアプリケーションを初期化する。

        :param RepositoryPersonSnapshotReidQueue repository_person_snapshot_reid_queue: 再識別キュー
        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        """
        self.repository_person_snapshot_reid_queue = repository_person_snapshot_reid_queue
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "BackgroundApplicationPersonSnapshotReid":
        """
        環境変数からバックグラウンドアプリケーションインスタンスを生成する。

        :param Environment environment: 環境変数
        :return BackgroundApplicationPersonSnapshotReid: バックグラウンドアプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot_reid_queue=RepositoryPersonSnapshotReidQueue.create(
                environment),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def reid(self) -> DtoPersonSnapshotPersonId:
        """
        再識別キューから1件取り出し、最近傍と照合して person_id を保存し、DTOを返す。

        :return DtoPersonSnapshotPersonId: 処理した人物検出結果のID・person_id・is_junk
        """
        person_snapshot_feature = self.repository_person_snapshot_reid_queue.pop()
        nearest_person_snapshot_feature = self.repository_person_snapshot.find_features_by_nearest(
            person_snapshot_feature)
        reid_person_snapshot_feature = person_snapshot_feature.reid(
            nearest_person_snapshot_feature)
        self.repository_person_snapshot.save_feature(
            reid_person_snapshot_feature)
        return DtoPersonSnapshotPersonId(
            id=reid_person_snapshot_feature.id.id,
            person_id=reid_person_snapshot_feature.person_id.id.id if reid_person_snapshot_feature.person_id.id is not None else None,
            is_junk=reid_person_snapshot_feature.person_id.is_junk,
        )
