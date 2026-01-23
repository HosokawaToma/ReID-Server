from modules.yolo.instance_segmenter import ModuleYoloInstanceSegmenter
from domain.yolo.instance_segmenter import DomainYoloInstanceSegmenter
from typing import ClassVar

class RepositoryYoloInstanceSegmenter:
    CACHE: ClassVar[ModuleYoloInstanceSegmenter | None] = None

    def __init__(self):
        if RepositoryYoloInstanceSegmenter.CACHE is None:
            RepositoryYoloInstanceSegmenter.CACHE = ModuleYoloInstanceSegmenter()
        self.model = RepositoryYoloInstanceSegmenter.CACHE

    @classmethod
    def create(cls) -> "RepositoryYoloInstanceSegmenter":
        return cls()

    def find(self) -> DomainYoloInstanceSegmenter:
        return DomainYoloInstanceSegmenter(model=self.model)
