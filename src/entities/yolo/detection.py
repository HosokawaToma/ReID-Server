from dataclasses import dataclass

@dataclass
class EntityYoloDetection:
    class_id: int
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float
