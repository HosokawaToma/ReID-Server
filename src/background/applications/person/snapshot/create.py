from repositories.person.snapshot.create_queue import RepositoryPersonSnapshotCreateQueue
from repositories.person.snapshot.reid_queue import RepositoryPersonSnapshotReidQueue
from environment import Environment
from error import Error
from background.applications.utils import BackgroundApplicationUtilsBase
from domain.yolo.object_detector import DomainYoloObjectDetector
from domain.yolo.instance_segmenter import DomainYoloInstanceSegmenter
from domain.yolo.pose_estimator import DomainYoloPoseEstimator

class BackgroundApplicationPersonSnapshotCreateError(Error):
    pass

class BackgroundApplicationPersonSnapshotCreate(BackgroundApplicationUtilsBase):
    def __init__(
        self,
        repository_person_snapshot_create_queue: RepositoryPersonSnapshotCreateQueue,
        repository_person_snapshot_reid_queue: RepositoryPersonSnapshotReidQueue,
        domain_yolo_object_detector: DomainYoloObjectDetector,
        domain_yolo_instance_segmenter: DomainYoloInstanceSegmenter,
        domain_yolo_pose_estimator: DomainYoloPoseEstimator,
    ):
        self.repository_person_snapshot_create_queue = repository_person_snapshot_create_queue
        self.domain_yolo_object_detector = domain_yolo_object_detector
        self.domain_yolo_instance_segmenter = domain_yolo_instance_segmenter
        self.domain_yolo_pose_estimator = domain_yolo_pose_estimator
        self.repository_person_snapshot_reid_queue = repository_person_snapshot_reid_queue

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundApplicationPersonSnapshotCreate":
        return cls(
            repository_person_snapshot_create_queue=RepositoryPersonSnapshotCreateQueue.create(
                environment),
            domain_yolo_object_detector=DomainYoloObjectDetector(),
            domain_yolo_instance_segmenter=DomainYoloInstanceSegmenter(),
            domain_yolo_pose_estimator=DomainYoloPoseEstimator(),
            repository_person_snapshot_reid_queue=RepositoryPersonSnapshotReidQueue.create(
                environment),
        )

    def save(self) -> None:
        try:
            frame_image = self.repository_person_snapshot_create_queue.pop()
            person_snapshots = frame_image.create_person_snapshot_images(
                yolo_object_detector=self.domain_yolo_object_detector,
                yolo_instance_segmenter=self.domain_yolo_instance_segmenter,
                yolo_pose_estimator=self.domain_yolo_pose_estimator,
            )
            self.repository_person_snapshot_reid_queue.push_all(person_snapshots)
        except Error as error:
            raise BackgroundApplicationPersonSnapshotCreateError(error) from error
