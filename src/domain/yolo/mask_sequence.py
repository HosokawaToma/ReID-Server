from dataclasses import dataclass
from domain.yolo.mask import DomainYoloMask
from domain.utils.sequence_base import DomainUtilsSequenceBase

@dataclass(frozen=True)
class DomainYoloMaskSequence(DomainUtilsSequenceBase[DomainYoloMask]):
    """
    YOLOのマスクのシーケンスのドメインモデル
    """
    def is_one_person(self) -> bool:
        return len(self.items) == 1
