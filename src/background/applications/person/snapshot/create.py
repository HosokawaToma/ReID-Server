"""
人物検出作成のバックグラウンドアプリケーション

キューからカメラフレームを1件取り出し、人物検出・再識別キュー投入・DTO返却を行う。
"""
from repositories.person.snapshot.create_queue import RepositoryPersonSnapshotCreateQueue
from repositories.person.snapshot.reid_queue import RepositoryPersonSnapshotReidQueue
from environment import Environment
from background.applications.utils import BackgroundApplicationUtilsBase
from repositories.yolo.object_detector import RepositoryYoloObjectDetector
from repositories.yolo.instance_segmenter import RepositoryYoloInstanceSegmenter
from repositories.yolo.pose_estimator import RepositoryYoloPoseEstimator
from dto.person.snapshot.detail import DtoPersonSnapshotDetail
from repositories.reid import RepositoryReID


class BackgroundApplicationPersonSnapshotCreate(BackgroundApplicationUtilsBase):
    """
    人物検出を1件作成するバックグラウンドアプリケーションクラス。

    人物検出キューからフレームを取得し、YOLO・ReIDで人物検出して再識別キューに投入する。
    """

    def __init__(
        self,
        repository_person_snapshot_create_queue: RepositoryPersonSnapshotCreateQueue,
        repository_person_snapshot_reid_queue: RepositoryPersonSnapshotReidQueue,
        repository_yolo_object_detector: RepositoryYoloObjectDetector,
        repository_yolo_instance_segmenter: RepositoryYoloInstanceSegmenter,
        repository_yolo_pose_estimator: RepositoryYoloPoseEstimator,
        repository_reid: RepositoryReID,
    ):
        """
        バックグラウンドアプリケーションを初期化する。

        :param RepositoryPersonSnapshotCreateQueue repository_person_snapshot_create_queue: 人物検出作成キュー
        :param RepositoryPersonSnapshotReidQueue repository_person_snapshot_reid_queue: 再識別キュー
        :param RepositoryYoloObjectDetector repository_yolo_object_detector: YOLO物体検出リポジトリ
        :param RepositoryYoloInstanceSegmenter repository_yolo_instance_segmenter: YOLOインスタンスセグメンテーションリポジトリ
        :param RepositoryYoloPoseEstimator repository_yolo_pose_estimator: YOLOポーズ推定リポジトリ
        :param RepositoryReID repository_reid: ReIDリポジトリ
        """
        self.repository_person_snapshot_create_queue = repository_person_snapshot_create_queue
        self.repository_yolo_object_detector = repository_yolo_object_detector
        self.repository_yolo_instance_segmenter = repository_yolo_instance_segmenter
        self.repository_yolo_pose_estimator = repository_yolo_pose_estimator
        self.repository_reid = repository_reid
        self.repository_person_snapshot_reid_queue = repository_person_snapshot_reid_queue

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundApplicationPersonSnapshotCreate":
        """
        環境からバックグラウンドアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return BackgroundApplicationPersonSnapshotCreate: バックグラウンドアプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot_create_queue=RepositoryPersonSnapshotCreateQueue.create(
                environment),
            repository_yolo_object_detector=RepositoryYoloObjectDetector.create(),
            repository_yolo_instance_segmenter=RepositoryYoloInstanceSegmenter.create(),
            repository_yolo_pose_estimator=RepositoryYoloPoseEstimator.create(),
            repository_reid=RepositoryReID.create(),
            repository_person_snapshot_reid_queue=RepositoryPersonSnapshotReidQueue.create(
                environment),
        )

    def save(self) -> list[DtoPersonSnapshotDetail]:
        """
        人物検出キューから1件取り出し、人物検出を実行して再識別キューに投入し、作成した人物検出のDTO一覧を返す。

        :return list[DtoPersonSnapshotDetail]: 作成した人物検出結果のDTO一覧
        """
        frame_image = self.repository_person_snapshot_create_queue.pop()
        person_snapshots = frame_image.create_person_snapshot_images(
            yolo_object_detector=self.repository_yolo_object_detector.find(),
            yolo_instance_segmenter=self.repository_yolo_instance_segmenter.find(),
            yolo_pose_estimator=self.repository_yolo_pose_estimator.find(),
            reid_model=self.repository_reid.find(),
        )
        self.repository_person_snapshot_reid_queue.push_all(person_snapshots)
        return [
            DtoPersonSnapshotDetail(
                id=person_snapshot.id.id,
                camera_id=person_snapshot.location.camera_id,
                view_id=person_snapshot.location.view_id,
                timestamp=person_snapshot.timestamp.timestamp,
                person_id=person_snapshot.person_id.id.id if person_snapshot.person_id.id is not None else None,
                is_junk=person_snapshot.person_id.is_junk,
            ) for person_snapshot in person_snapshots
        ]
