"""
YOLO キーポイントシーケンスのドメインモデル

複数人分のキーポイントを保持し、1人のみの取得・1人判定を提供する。
"""
from dataclasses import dataclass
from domain.yolo.key_points import DomainYoloKeyPoints
from domain.utils.sequence_base import DomainUtilsSequenceBase


@dataclass(frozen=True)
class DomainYoloKeyPointsSequence(DomainUtilsSequenceBase[DomainYoloKeyPoints]):
    """
    YOLO のキーポイントのシーケンスを保持するドメインモデル。
    """

    def one_person(self) -> DomainYoloKeyPoints:
        """
        1人分のキーポイントを返す。1人でない場合は ValueError。

        :return DomainYoloKeyPoints: キーポイント
        :raises ValueError: 人数が1人でない場合
        """
        if len(self.items) != 1:
            raise ValueError("キーポイントのシーケンスには1人のみが含まれている必要があります")
        return self.items[0]

    def is_one_person(self) -> bool:
        """
        キーポイントが1人分のみかどうかを返す。

        :return bool: 1人分のみなら True
        """
        return len(self.items) == 1
