from dataclasses import dataclass
from domain.person.snapshot.image import DomainPersonSnapshotImage
from domain.utils.sequence_base import DomainUtilsSequenceBase
from domain.yolo.instance_segmenter import DomainYoloInstanceSegmenter
from domain.yolo.pose_estimator import DomainYoloPoseEstimator

@dataclass
class DomainPersonSnapshotImageSequence(DomainUtilsSequenceBase[DomainPersonSnapshotImage]):
    """
    人物検出結果の画像のシーケンスのドメインモデル
    """

    def detect_junk(self, instance_segmenter: DomainYoloInstanceSegmenter, pose_estimator: DomainYoloPoseEstimator) -> None:
        for person_snapshot_image in self.items:
            person_snapshot_image.detect_junk(instance_segmenter, pose_estimator)
