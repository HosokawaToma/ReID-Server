from dataclasses import dataclass
from PIL import Image
import io
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
    bytes: bytes
    format: str

    @classmethod
    def from_image(cls, image: Image.Image) -> "DomainImage":
        if image.format is None:
            raise ValueError("画像のフォーマットが不明です")
        buffer = io.BytesIO()
        image.save(buffer, format=image.format)
        return cls(bytes=buffer.getvalue(), format=image.format)

    @property
    def image(self) -> Image.Image:
        return Image.open(io.BytesIO(self.bytes))

    def detect_person(self, detection_model: DomainYoloObjectDetector) -> DomainYoloBoundingBoxSequence:
        return detection_model.extract_person(self.image)

    def extract_instance(self, instance_segmenter: DomainYoloInstanceSegmenter) -> DomainYoloMaskSequence:
        return instance_segmenter.extract(self.image)

    def extract_pose(self, pose_estimator: DomainYoloPoseEstimator) -> DomainYoloKeyPointsSequence:
        return pose_estimator.extract(self.image)

    def crop(self, x1: float, y1: float, x2: float, y2: float) -> "DomainImage":
        image = self.image.crop((x1, y1, x2, y2))
        return DomainImage.from_image(image)
