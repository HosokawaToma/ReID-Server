from domain.yolo.pose_estimator import DomainYoloPoseEstimator
from typing import ClassVar
from ultralytics.models.yolo import YOLO

class RepositoryYoloPoseEstimator:
    WEIGHTS_PATH: ClassVar[str] = "./resources/models/yolo11x-pose.pt"
    CACHE: ClassVar[DomainYoloPoseEstimator] | None = None

    def __init__(self):
        if RepositoryYoloPoseEstimator.CACHE is None:
            RepositoryYoloPoseEstimator.CACHE = DomainYoloPoseEstimator(
                model=YOLO(RepositoryYoloPoseEstimator.WEIGHTS_PATH),
            )
        self.yolo_pose_estimator = RepositoryYoloPoseEstimator.CACHE

    @classmethod
    def create(cls) -> "RepositoryYoloPoseEstimator":
        return cls()

    def get_instance(self) -> DomainYoloPoseEstimator:
        return self.yolo_pose_estimator
