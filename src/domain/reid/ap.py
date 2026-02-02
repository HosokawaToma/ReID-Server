from dataclasses import dataclass
from domain.reid.rank_sequence import DomainReidRankSequence
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainReidAp(DomainUtilsBase):
    """
    APのドメインモデル
    """
    ap: float

    @classmethod
    def calculate(cls, ranking_sequence: DomainReidRankSequence) -> "DomainReidAp":
        """
        APを計算する
        :param DomainReidRankSequence ranking_sequence: ランキングシーケンス
        :return DomainReidAp: AP
        """
        ap = 0.0
        ranking_sequence = ranking_sequence.sort_by_rank()
        for i, ranking in enumerate(ranking_sequence):
            ap += (i + 1) / ranking.rank
        return cls(ap=ap / len(ranking_sequence.items))
