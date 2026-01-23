from repositories.person.snapshot.create_queue import RepositoryPersonSnapshotCreateQueue
from repositories.person.snapshot.reid_queue import RepositoryPersonSnapshotReidQueue
from repositories.yolo.detector import RepositoryYoloDetector
from repositories.yolo.instance_segmenter import RepositoryYoloInstanceSegmenter
from repositories.yolo.pose_estimator import RepositoryYoloPoseEstimator
from dto.frame_image.meta_data import DtoFrameImageMetaData
from environment import Environment
from error import Error
from background.applications.utils import BackgroundApplicationUtilsBase

class BackgroundApplicationPersonSnapshotCreateError(Error):
    pass

class BackgroundApplicationPersonSnapshotCreate(BackgroundApplicationUtilsBase):
    def __init__(
        self,
        repository_person_snapshot_create_queue: RepositoryPersonSnapshotCreateQueue,
        repository_yolo_detector: RepositoryYoloDetector,
        repository_yolo_instance_segmenter: RepositoryYoloInstanceSegmenter,
        repository_yolo_pose_estimator: RepositoryYoloPoseEstimator,
        repository_person_snapshot_reid_queue: RepositoryPersonSnapshotReidQueue,
    ):
        self.repository_person_snapshot_create_queue = repository_person_snapshot_create_queue
        self.repository_yolo_detector = repository_yolo_detector
        self.repository_yolo_instance_segmenter = repository_yolo_instance_segmenter
        self.repository_yolo_pose_estimator = repository_yolo_pose_estimator
        self.repository_person_snapshot_reid_queue = repository_person_snapshot_reid_queue

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundApplicationPersonSnapshotCreate":
        return cls(
            repository_person_snapshot_create_queue=RepositoryPersonSnapshotCreateQueue.create(
                environment),
            repository_yolo_detector=RepositoryYoloDetector.create(),
            repository_yolo_instance_segmenter=RepositoryYoloInstanceSegmenter.create(),
            repository_yolo_pose_estimator=RepositoryYoloPoseEstimator.create(),
            repository_person_snapshot_reid_queue=RepositoryPersonSnapshotReidQueue.create(
                environment),
        )

    def save(self) -> DtoFrameImageMetaData:
        try:
            frame_image = self.repository_person_snapshot_create_queue.pop()
            yolo_object_detector = self.repository_yolo_detector.get_instance()
            yolo_instance_segmenter = self.repository_yolo_instance_segmenter.get_instance()
            yolo_pose_estimator = self.repository_yolo_pose_estimator.get_instance()
            person_snapshots = frame_image.create_person_snapshot_images(
                yolo_object_detector=yolo_object_detector,
                yolo_instance_segmenter=yolo_instance_segmenter,
                yolo_pose_estimator=yolo_pose_estimator,
            )
            self.repository_person_snapshot_reid_queue.push_all(person_snapshots)
            return DtoFrameImageMetaData(
                id=frame_image.id.id,
                camera_id=frame_image.location.camera_id,
                view_id=frame_image.location.view_id,
                timestamp=frame_image.timestamp.timestamp,
            )
        except Error as error:
            raise BackgroundApplicationPersonSnapshotCreateError(error) from error
