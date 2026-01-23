from domain.yolo.instance_segmenter import DomainYoloInstanceSegmenter
from typing import ClassVar
from ultralytics.models.yolo import YOLO


class RepositoryYoloInstanceSegmenter:
    WEIGHTS_PATH: ClassVar[str] = "./resources/models/yolo11x-instance-segmenter.pt"
    CACHE: ClassVar[DomainYoloInstanceSegmenter] | None = None

    def __init__(self):
        if self.CACHE is None:
            self.CACHE = DomainYoloInstanceSegmenter(
                model=YOLO(self.WEIGHTS_PATH),
            )
        self.yolo_instance_segmenter = self.CACHE

    @classmethod
    def create(cls) -> "RepositoryYoloInstanceSegmenter":
        return cls()

    def get_instance(self) -> DomainYoloInstanceSegmenter:
        return self.yolo_instance_segmenter
