from modules.yolo.object_detector import ModuleYoloObjectDetector
from domain.yolo.object_detector import DomainYoloObjectDetector
from typing import ClassVar


class RepositoryYoloObjectDetector:
    CACHE: ClassVar[ModuleYoloObjectDetector | None] = None

    def __init__(self):
        if RepositoryYoloObjectDetector.CACHE is None:
            RepositoryYoloObjectDetector.CACHE = ModuleYoloObjectDetector()
        self.model = RepositoryYoloObjectDetector.CACHE

    @classmethod
    def create(cls) -> "RepositoryYoloObjectDetector":
        return cls()

    def find(self) -> DomainYoloObjectDetector:
        return DomainYoloObjectDetector(model=self.model)
