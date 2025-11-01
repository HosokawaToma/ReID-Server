from dataclasses import dataclass
from typing import List

@dataclass
class EntityYoloKeypoints:
    keypoints: List[tuple[float, float]]
    confidences: List[float]
