from dataclasses import dataclass
from domain.yolo.mask import DomainYoloMask
from domain.utils.sequence_base import DomainUtilsSequenceBase


@dataclass(frozen=True)
class DomainYoloMaskSequence(DomainUtilsSequenceBase[DomainYoloMask]):
    """
    YOLOのマスクのシーケンスのドメインモデル
    """

    def is_one_person(self) -> bool:
        """
        マスクが1件のみ（1人分の検出）かどうかを返す。

        :return bool: 1件のみならTrue
        """
        return len(self.items) == 1
