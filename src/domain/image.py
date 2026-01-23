from dataclasses import dataclass
from PIL import Image
from domain.yolo.object_detector import DomainYoloObjectDetector
from domain.yolo.bounding_box_sequence import DomainYoloBoundingBoxSequence
from domain.yolo.mask_sequence import DomainYoloMaskSequence
from domain.yolo.instance_segmenter import DomainYoloInstanceSegmenter
from domain.yolo.pose_estimator import DomainYoloPoseEstimator
from domain.yolo.key_points_sequence import DomainYoloKeyPointsSequence
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainImage(DomainUtilsBase):
    """
    画像のドメインモデル
    """
    image: Image.Image
    format: str

    def __post_init__(self):
        """
        不変性維持のため画像をコピーします
        """
        object.__setattr__(self, "image", self.image.copy())

    def detect_person(self, detection_model: DomainYoloObjectDetector) -> DomainYoloBoundingBoxSequence:
        return detection_model.extract_person(self.image)

    def extract_instance(self, instance_segmenter: DomainYoloInstanceSegmenter) -> DomainYoloMaskSequence:
        return instance_segmenter.extract(self.image)

    def extract_pose(self, pose_estimator: DomainYoloPoseEstimator) -> DomainYoloKeyPointsSequence:
        return pose_estimator.extract(self.image)

    def crop(self, x1: float, y1: float, x2: float, y2: float) -> "DomainImage":
        image = self.image.crop((x1, y1, x2, y2))
        return DomainImage(image=image, format=self.format)
