from repositories.person.snapshot.create_queue import RepositoryPersonSnapshotCreateQueue
from repositories.person.snapshot.reid_queue import RepositoryPersonSnapshotReidQueue
from environment import Environment
from error import Error
from background.applications.utils import BackgroundApplicationUtilsBase
from repositories.yolo.object_detector import RepositoryYoloObjectDetector
from repositories.yolo.instance_segmenter import RepositoryYoloInstanceSegmenter
from repositories.yolo.pose_estimator import RepositoryYoloPoseEstimator

class BackgroundApplicationPersonSnapshotCreateError(Error):
    pass

class BackgroundApplicationPersonSnapshotCreate(BackgroundApplicationUtilsBase):
    def __init__(
        self,
        repository_person_snapshot_create_queue: RepositoryPersonSnapshotCreateQueue,
        repository_person_snapshot_reid_queue: RepositoryPersonSnapshotReidQueue,
        repository_yolo_object_detector: RepositoryYoloObjectDetector,
        repository_yolo_instance_segmenter: RepositoryYoloInstanceSegmenter,
        repository_yolo_pose_estimator: RepositoryYoloPoseEstimator,
    ):
        self.repository_person_snapshot_create_queue = repository_person_snapshot_create_queue
        self.repository_yolo_object_detector = repository_yolo_object_detector
        self.repository_yolo_instance_segmenter = repository_yolo_instance_segmenter
        self.repository_yolo_pose_estimator = repository_yolo_pose_estimator
        self.repository_person_snapshot_reid_queue = repository_person_snapshot_reid_queue

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundApplicationPersonSnapshotCreate":
        return cls(
            repository_person_snapshot_create_queue=RepositoryPersonSnapshotCreateQueue.create(
                environment),
            repository_yolo_object_detector=RepositoryYoloObjectDetector.create(),
            repository_yolo_instance_segmenter=RepositoryYoloInstanceSegmenter.create(),
            repository_yolo_pose_estimator=RepositoryYoloPoseEstimator.create(),
            repository_person_snapshot_reid_queue=RepositoryPersonSnapshotReidQueue.create(
                environment),
        )

    def save(self) -> None:
        try:
            frame_image = self.repository_person_snapshot_create_queue.pop()
            person_snapshots = frame_image.create_person_snapshot_images(
                yolo_object_detector=self.repository_yolo_object_detector.find(),
                yolo_instance_segmenter=self.repository_yolo_instance_segmenter.find(),
                yolo_pose_estimator=self.repository_yolo_pose_estimator.find(),
            )
            self.repository_person_snapshot_reid_queue.push_all(person_snapshots)
        except Error as error:
            raise BackgroundApplicationPersonSnapshotCreateError(error) from error
