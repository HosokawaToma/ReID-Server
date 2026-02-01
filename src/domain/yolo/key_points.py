from dataclasses import dataclass
from domain.yolo.key_point import DomainYoloKeyPoint
from typing import ClassVar
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainYoloKeyPoints(DomainUtilsBase):
    """
    YOLOのキーポイントのドメインモデル
    """
    nose: DomainYoloKeyPoint
    left_eye: DomainYoloKeyPoint
    right_eye: DomainYoloKeyPoint
    left_ear: DomainYoloKeyPoint
    right_ear: DomainYoloKeyPoint
    left_shoulder: DomainYoloKeyPoint
    right_shoulder: DomainYoloKeyPoint
    left_elbow: DomainYoloKeyPoint
    right_elbow: DomainYoloKeyPoint
    left_wrist: DomainYoloKeyPoint
    right_wrist: DomainYoloKeyPoint
    left_hip: DomainYoloKeyPoint
    right_hip: DomainYoloKeyPoint
    left_knee: DomainYoloKeyPoint
    right_knee: DomainYoloKeyPoint
    left_ankle: DomainYoloKeyPoint
    right_ankle: DomainYoloKeyPoint

    UPPER_BODY_CONFIDENCE_THRESHOLD: ClassVar[float] = 0.65
    LOWER_BODY_CONFIDENCE_THRESHOLD: ClassVar[float] = 0.65

    @property
    def upper_body_key_points(self) -> list[DomainYoloKeyPoint]:
        return [
            self.left_shoulder,
            self.right_shoulder,
            self.left_elbow,
            self.right_elbow,
            self.left_wrist,
            self.right_wrist,
        ]

    @property
    def lower_body_key_points(self) -> list[DomainYoloKeyPoint]:
        return [
            self.left_hip,
            self.right_hip,
            self.left_knee,
            self.right_knee,
            self.left_ankle,
            self.right_ankle,
        ]

    def is_full_length(self) -> bool:
        upper_body_key_points = self.upper_body_key_points
        if sum([key_point.confidence for key_point in upper_body_key_points]) / len(upper_body_key_points) < self.UPPER_BODY_CONFIDENCE_THRESHOLD:
            return False
        lower_body_key_points = self.lower_body_key_points
        if sum([key_point.confidence for key_point in lower_body_key_points]) / len(lower_body_key_points) < self.LOWER_BODY_CONFIDENCE_THRESHOLD:
            return False
        return True
