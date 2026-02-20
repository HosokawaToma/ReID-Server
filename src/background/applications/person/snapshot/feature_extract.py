"""
人物検出特徴量抽出のバックグラウンドアプリケーション

キューから1件取り出し、特徴量を再抽出して保存し、処理したIDのDTOを返す。
"""
from repositories.person.snapshot.feature_extract_queue import RepositoryPersonSnapshotFeatureExtractQueue
from repositories.reid import RepositoryReID
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from background.applications.utils import BackgroundApplicationUtilsBase
from dto.id import DtoId


class BackgroundApplicationPersonSnapshotFeatureExtract(BackgroundApplicationUtilsBase):
    """
    人物検出の特徴量を1件再抽出するバックグラウンドアプリケーションクラス。
    """

    def __init__(
        self,
        repository_person_snapshot_feature_extract_queue: RepositoryPersonSnapshotFeatureExtractQueue,
        repository_reid: RepositoryReID,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        """
        バックグラウンドアプリケーションを初期化する。

        :param RepositoryPersonSnapshotFeatureExtractQueue repository_person_snapshot_feature_extract_queue: 特徴量抽出キュー
        :param RepositoryReID repository_reid: ReIDリポジトリ
        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        """
        self.repository_person_snapshot_feature_extract_queue = repository_person_snapshot_feature_extract_queue
        self.repository_reid = repository_reid
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundApplicationPersonSnapshotFeatureExtract":
        """
        環境からバックグラウンドアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return BackgroundApplicationPersonSnapshotFeatureExtract: バックグラウンドアプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot_feature_extract_queue=RepositoryPersonSnapshotFeatureExtractQueue.create(
                environment),
            repository_reid=RepositoryReID.create(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def extract(self) -> DtoId:
        """
        特徴量抽出キューから1件取り出し、特徴量を再抽出して保存し、処理したIDのDTOを返す。

        :return DtoId: 処理した人物検出結果のID
        """
        person_snapshot_image = self.repository_person_snapshot_feature_extract_queue.pop()
        feature = person_snapshot_image.re_extract_feature(
            reid_model=self.repository_reid.find())
        self.repository_person_snapshot.save_feature(feature)
        return DtoId(id=feature.id.id)
