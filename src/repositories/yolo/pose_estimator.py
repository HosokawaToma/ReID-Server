from domain.yolo.pose_estimator import DomainYoloPoseEstimator
from typing import ClassVar
from ultralytics.models.yolo import YOLO

class RepositoryYoloPoseEstimator:
    WEIGHTS_PATH: ClassVar[str] = "./resources/models/yolo11x-pose.pt"
    CACHE: ClassVar[DomainYoloPoseEstimator] | None = None

    def __init__(self):
        if self.CACHE is None:
            self.CACHE = DomainYoloPoseEstimator(
                model=YOLO(self.WEIGHTS_PATH),
            )
        self.yolo_pose_estimator = self.CACHE

    @classmethod
    def create(cls) -> "RepositoryYoloPoseEstimator":
        return cls()

    def get_instance(self) -> DomainYoloPoseEstimator:
        return self.yolo_pose_estimator
