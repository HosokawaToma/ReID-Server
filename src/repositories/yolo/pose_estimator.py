from modules.yolo.pose_estimator import ModuleYoloPoseEstimator
from domain.yolo.pose_estimator import DomainYoloPoseEstimator
from typing import ClassVar


class RepositoryYoloPoseEstimator:
    CACHE: ClassVar[ModuleYoloPoseEstimator | None] = None

    def __init__(self):
        if RepositoryYoloPoseEstimator.CACHE is None:
            RepositoryYoloPoseEstimator.CACHE = ModuleYoloPoseEstimator()
        self.model = RepositoryYoloPoseEstimator.CACHE

    @classmethod
    def create(cls) -> "RepositoryYoloPoseEstimator":
        return cls()

    def find(self) -> DomainYoloPoseEstimator:
        return DomainYoloPoseEstimator(model=self.model)
