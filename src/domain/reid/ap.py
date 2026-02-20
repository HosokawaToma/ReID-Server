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
    ReID の平均精度（AP）のドメインモデル。

    1 クエリについて、類似度順に並んだランキングから算出した AP を保持する。0 以上 1 以下の浮動小数点。
    """
    ap: float

    @classmethod
    def calculate(
        cls,
        ranking_sequence: DomainReidRankSequence,
    ) -> "DomainReidAp":
        """
        類似度順に並んだランキングシーケンスから AP を算出し、その値を保持するインスタンスを返す。

        ランキングが空の場合は 0 とする。正解のランクの逆数和の平均で計算する。

        :param DomainReidRankSequence ranking_sequence: クエリに対する類似度順のランキング
        :return DomainReidAp: 算出した AP
        """
        ap = 0.0
        if len(ranking_sequence) == 0:
            return cls(ap=0.0)
        for i, ranking in enumerate(ranking_sequence):
            ap += (i + 1) / ranking.rank
        return cls(ap=ap / len(ranking_sequence))
