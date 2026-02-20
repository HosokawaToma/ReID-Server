"""
人物検出ジャンク判定のバックグラウンドアプリケーション

キューから1件取り出し、再判定して person_id を保存し、処理したIDのDTOを返す。
"""
from background.applications.utils import BackgroundApplicationUtilsBase
from repositories.person.snapshot.detect_junk_queue import RepositoryPersonSnapshotDetectJunkQueue
from environment import Environment
from repositories.yolo.instance_segmenter import RepositoryYoloInstanceSegmenter
from repositories.yolo.pose_estimator import RepositoryYoloPoseEstimator
from repositories.person.snapshot import RepositoryPersonSnapshot
from domain.person.snapshot.person_id import DomainPersonSnapshotPersonId
from dto.id import DtoId


class BackgroundApplicationPersonSnapshotDetectJunk(BackgroundApplicationUtilsBase):
    """
    人物検出のジャンクを1件再判定するバックグラウンドアプリケーションクラス。
    """

    def __init__(
        self,
        repository_person_snapshot_detect_junk_queue: RepositoryPersonSnapshotDetectJunkQueue,
        repository_yolo_instance_segmenter: RepositoryYoloInstanceSegmenter,
        repository_yolo_pose_estimator: RepositoryYoloPoseEstimator,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        """
        バックグラウンドアプリケーションを初期化する。

        :param RepositoryPersonSnapshotDetectJunkQueue repository_person_snapshot_detect_junk_queue: ジャンク判定キュー
        :param RepositoryYoloInstanceSegmenter repository_yolo_instance_segmenter: YOLOインスタンスセグメンテーション
        :param RepositoryYoloPoseEstimator repository_yolo_pose_estimator: YOLOポーズ推定
        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        """
        self.repository_person_snapshot_detect_junk_queue = repository_person_snapshot_detect_junk_queue
        self.repository_yolo_instance_segmenter = repository_yolo_instance_segmenter
        self.repository_yolo_pose_estimator = repository_yolo_pose_estimator
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundApplicationPersonSnapshotDetectJunk":
        """
        環境からバックグラウンドアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return BackgroundApplicationPersonSnapshotDetectJunk: バックグラウンドアプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot_detect_junk_queue=RepositoryPersonSnapshotDetectJunkQueue.create(
                environment),
            repository_yolo_instance_segmenter=RepositoryYoloInstanceSegmenter.create(),
            repository_yolo_pose_estimator=RepositoryYoloPoseEstimator.create(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def detect_junk(self) -> DtoId:
        """
        人物検出結果のゴミデータを再判定する
        :return DtoId: 人物検出結果のゴミデータを再判定した人物ID
        """
        person_snapshot = self.repository_person_snapshot_detect_junk_queue.pop()
        person_snapshot = person_snapshot.re_detect_junk(
            instance_segmenter=self.repository_yolo_instance_segmenter.find(),
            pose_estimator=self.repository_yolo_pose_estimator.find(),
        )
        self.repository_person_snapshot.save_person_id(
            person_snapshot_person_id=DomainPersonSnapshotPersonId(
                id=person_snapshot.id,
                person_id=person_snapshot.person_id,
            ),
        )
        return DtoId(
            id=person_snapshot.id.id,
        )
