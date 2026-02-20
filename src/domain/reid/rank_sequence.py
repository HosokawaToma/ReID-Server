"""
ReID ランクシーケンスのドメインモデル

ランクのリストを保持し、最小ランク取得・ランク順ソートを提供する。
"""
from dataclasses import dataclass
from domain.reid.rank import DomainReidRank
from domain.utils.sequence_base import DomainUtilsSequenceBase
from error import ValidationError


@dataclass(frozen=True)
class DomainReidRankSequence(DomainUtilsSequenceBase[DomainReidRank]):
    """
    再識別評価のランクのシーケンスのドメインモデル
    """
    def top_rank(self) -> int:
        """
        最小のランクを取得する
        :return int: 最小のランク
        """
        if len(self.items) == 0:
            raise ValidationError(f"ランクのシーケンスには1人以上が含まれている必要があります: {len(self.items)}")
        return min(rank.rank for rank in self.items)

    def sort_by_rank(self) -> "DomainReidRankSequence":
        """
        ランクでソートする
        :return DomainReidRankSequence: ランクでソートしたシーケンス
        """
        return DomainReidRankSequence(items=sorted(self.items, key=lambda x: x.rank))
