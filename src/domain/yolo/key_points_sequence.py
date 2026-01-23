from dataclasses import dataclass
from domain.yolo.key_points import DomainYoloKeyPoints
from domain.utils.sequence_base import DomainUtilsSequenceBase

@dataclass
class DomainYoloKeyPointsSequence(DomainUtilsSequenceBase[DomainYoloKeyPoints]):
    """
    YOLOのキーポイントのシーケンスのドメインモデル
    """
    def one_person(self) -> DomainYoloKeyPoints:
        if len(self.items) != 1:
            raise ValueError("キーポイントのシーケンスには1人のみが含まれている必要があります")
        return self.items[0]
