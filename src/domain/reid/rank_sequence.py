from dataclasses import dataclass
from domain.reid.rank import DomainReidRank
from domain.utils.sequence_base import DomainUtilsSequenceBase

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
        return min(rank.rank for rank in self.items)
