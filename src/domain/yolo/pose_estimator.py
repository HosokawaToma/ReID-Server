from domain.yolo.key_points_sequence import DomainYoloKeyPointsSequence
from domain.yolo.key_points import DomainYoloKeyPoints
from domain.yolo.key_point import DomainYoloKeyPoint
from domain.image import DomainImage
from dataclasses import dataclass, field
from domain.utils.base import DomainUtilsBase
from modules.yolo.pose_estimator import ModuleYoloPoseEstimator


@dataclass(frozen=True)
class DomainYoloPoseEstimator(DomainUtilsBase):
    """
    YOLOの姿勢推定器のドメインモデル
    """
    model: ModuleYoloPoseEstimator = field(init=False, default_factory=ModuleYoloPoseEstimator)

    def extract(self, image: DomainImage) -> DomainYoloKeyPointsSequence:
        results = self.model.extract(image.image)
        key_points: list[DomainYoloKeyPoints] = []
        for item in results:
            if item.keypoints is None:
                continue
            xys = item.keypoints.xy[0].tolist()
            confs = item.keypoints.conf
            if confs is None:
                continue
            confs = confs.squeeze().tolist()
            key_points.append(DomainYoloKeyPoints(
                nose=DomainYoloKeyPoint(
                    x=xys[0][0],
                    y=xys[0][1],
                    confidence=confs[0],
                ),
                left_eye=DomainYoloKeyPoint(
                    x=xys[1][0],
                    y=xys[1][1],
                    confidence=confs[1],
                ),
                right_eye=DomainYoloKeyPoint(
                    x=xys[2][0],
                    y=xys[2][1],
                    confidence=confs[2],
                ),
                left_ear=DomainYoloKeyPoint(
                    x=xys[3][0],
                    y=xys[3][1],
                    confidence=confs[3],
                ),
                right_ear=DomainYoloKeyPoint(
                    x=xys[4][0],
                    y=xys[4][1],
                    confidence=confs[4],
                ),
                left_shoulder=DomainYoloKeyPoint(
                    x=xys[5][0],
                    y=xys[5][1],
                    confidence=confs[5],
                ),
                right_shoulder=DomainYoloKeyPoint(
                    x=xys[6][0],
                    y=xys[6][1],
                    confidence=confs[6],
                ),
                left_elbow=DomainYoloKeyPoint(
                    x=xys[7][0],
                    y=xys[7][1],
                    confidence=confs[7],
                ),
                right_elbow=DomainYoloKeyPoint(
                    x=xys[8][0],
                    y=xys[8][1],
                    confidence=confs[8],
                ),
                left_wrist=DomainYoloKeyPoint(
                    x=xys[9][0],
                    y=xys[9][1],
                    confidence=confs[9],
                ),
                right_wrist=DomainYoloKeyPoint(
                    x=xys[10][0],
                    y=xys[10][1],
                    confidence=confs[10],
                ),
                left_hip=DomainYoloKeyPoint(
                    x=xys[11][0],
                    y=xys[11][1],
                    confidence=confs[11],
                ),
                right_hip=DomainYoloKeyPoint(
                    x=xys[12][0],
                    y=xys[12][1],
                    confidence=confs[12],
                ),
                left_knee=DomainYoloKeyPoint(
                    x=xys[13][0],
                    y=xys[13][1],
                    confidence=confs[13],
                ),
                right_knee=DomainYoloKeyPoint(
                    x=xys[14][0],
                    y=xys[14][1],
                    confidence=confs[14],
                ),
                left_ankle=DomainYoloKeyPoint(
                    x=xys[15][0],
                    y=xys[15][1],
                    confidence=confs[15],
                ),
                right_ankle=DomainYoloKeyPoint(
                    x=xys[16][0],
                    y=xys[16][1],
                    confidence=confs[16],
                ),
            ))
        return DomainYoloKeyPointsSequence(items=key_points)
