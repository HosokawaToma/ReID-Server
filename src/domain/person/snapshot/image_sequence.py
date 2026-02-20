"""
人物スナップショット画像シーケンスのドメインモデル

人物検出画像のリストを保持し、一括ゴミ判定を提供する。
"""
from dataclasses import dataclass
from domain.person.snapshot.image import DomainPersonSnapshotImage
from domain.utils.sequence_base import DomainUtilsSequenceBase
from domain.yolo.instance_segmenter import DomainYoloInstanceSegmenter
from domain.yolo.pose_estimator import DomainYoloPoseEstimator


@dataclass(frozen=True)
class DomainPersonSnapshotImageSequence(DomainUtilsSequenceBase[DomainPersonSnapshotImage]):
    """
    人物検出結果の画像のシーケンスのドメインモデル
    """

    def detect_junk(self, instance_segmenter: DomainYoloInstanceSegmenter, pose_estimator: DomainYoloPoseEstimator) -> "DomainPersonSnapshotImageSequence":
        """
        人物検出結果の画像の集合からゴミデータを判定する
        :param DomainYoloInstanceSegmenter instance_segmenter: 個体推定器
        :param DomainYoloPoseEstimator pose_estimator: 姿勢推定器
        :return DomainPersonSnapshotImageSequence: ゴミデータを判定した人物検出結果の画像の集合
        """
        return DomainPersonSnapshotImageSequence(items=[
            person_snapshot_image.detect_junk(
                instance_segmenter, pose_estimator)
            for person_snapshot_image in self.items
        ])
