from dataclasses import dataclass
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.image import DomainImage
from domain.yolo.object_detector import DomainYoloObjectDetector
from domain.yolo.instance_segmenter import DomainYoloInstanceSegmenter
from domain.yolo.pose_estimator import DomainYoloPoseEstimator
from domain.person.snapshot.image_sequence import DomainPersonSnapshotImageSequence
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainCameraFrameImage(DomainUtilsBase):
    """
    カメラフレーム画像のドメインモデル
    """
    id: DomainId
    location: DomainLocation
    timestamp: DomainTimestamp
    image: DomainImage

    def create_person_snapshot_images(
        self,
        yolo_object_detector: DomainYoloObjectDetector,
        yolo_instance_segmenter: DomainYoloInstanceSegmenter,
        yolo_pose_estimator: DomainYoloPoseEstimator,
        ) -> DomainPersonSnapshotImageSequence:
        bounding_boxes = self.image.detect_person(yolo_object_detector)
        person_snapshot_images = bounding_boxes.create_person_snapshot_images(self)
        return person_snapshot_images.detect_junk(yolo_instance_segmenter, yolo_pose_estimator)
