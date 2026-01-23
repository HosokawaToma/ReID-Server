from domain.yolo.object_detector import DomainYoloObjectDetector
from typing import ClassVar
from ultralytics.models.yolo import YOLO

class RepositoryYoloDetector:
    WEIGHTS_PATH: ClassVar[str] = "./resources/models/yolo11x.pt"
    CACHE: ClassVar[DomainYoloObjectDetector] | None = None

    def __init__(self):
        if self.CACHE is None:
            self.CACHE = DomainYoloObjectDetector(
                model=YOLO(self.WEIGHTS_PATH),
            )
        self.yolo_object_detector = self.CACHE

    @classmethod
    def create(cls) -> "RepositoryYoloDetector":
        return cls()

    def get_instance(self) -> DomainYoloObjectDetector:
        return self.yolo_object_detector
