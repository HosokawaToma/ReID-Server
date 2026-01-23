from dataclasses import dataclass
from domain.yolo.bounding_box import DomainYoloBoundingBox
from domain.utils.sequence_base import DomainUtilsSequenceBase

@dataclass(frozen=True)
class DomainYoloBoundingBoxSequence(DomainUtilsSequenceBase[DomainYoloBoundingBox]):
    """
    YOLOのバウンディングボックスのシーケンスのドメインモデル
    """
