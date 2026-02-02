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
        for ranking in ranking_sequence.items:
            ap += 1.0 / ranking.rank
        return cls(ap=ap / len(ranking_sequence.items))
