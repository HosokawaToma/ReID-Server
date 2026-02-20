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

    CONFIDENCE_THRESHOLD: ClassVar[float] = 0.65

    def is_full_length(self) -> bool:
        """
        全キーポイントの平均信頼度が閾値以上かどうかを返す。
        全身が十分に検出されているとみなすかどうかの判定に用いる。

        :return bool: 閾値以上ならTrue
        """
        key_points = [
            self.nose,
            self.left_eye,
            self.right_eye,
            self.left_ear,
            self.right_ear,
            self.left_shoulder,
            self.right_shoulder,
            self.left_elbow,
            self.right_elbow,
            self.left_wrist,
            self.right_wrist,
            self.left_hip,
            self.right_hip,
            self.left_knee,
            self.right_knee,
            self.left_ankle,
            self.right_ankle,
        ]
        return sum([key_point.confidence for key_point in key_points]) / len(key_points) > self.CONFIDENCE_THRESHOLD
