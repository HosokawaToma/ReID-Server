from domain.yolo.pose_estimator import DomainYoloPoseEstimator
from typing import ClassVar

class RepositoryYoloPoseEstimator:
    WEIGHTS_PATH: ClassVar[str] = "./resources/models/yolo11x-pose.pt"
    CACHE: ClassVar[DomainYoloPoseEstimator] | None = None

    def __init__(self):
        if self.CACHE is None:
            self.CACHE = DomainYoloPoseEstimator(
                weights_path=self.WEIGHTS_PATH,
            )
        self.yolo_pose_estimator = self.CACHE

    @classmethod
    def create(cls) -> "RepositoryYoloPoseEstimator":
        return cls()

    def get_instance(self) -> DomainYoloPoseEstimator:
        return self.yolo_pose_estimator
