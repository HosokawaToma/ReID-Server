"""
ReID 平均精度（AP）のドメインモデル

ランキングシーケンスから AP を算出する。
"""
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
    def calculate(
        cls,
        ranking_sequence: DomainReidRankSequence,
    ) -> "DomainReidAp":
        """
        APを計算する
        :param DomainReidRankSequence ranking_sequence: ランキングシーケンス（クエリデータに対する類似度順に並んでいることが前提）
        :return DomainReidAp: AP
        """
        ap = 0.0
        if len(ranking_sequence) == 0:
            return cls(ap=0.0)
        for i, ranking in enumerate(ranking_sequence):
            ap += (i + 1) / ranking.rank
        return cls(ap=ap / len(ranking_sequence))
