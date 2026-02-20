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

        類似度の高い順に並べたギャラリー全体を 1 位から見ていき、各順位で「その順位までに含まれる正解の割合（適合率）」を求める。
        順位ごとに、その順位の画像が正解ならばその時点の適合率を足し、正解でなければ足さない。
        最後に、足し上げた値を正解画像の総数で割ったものが、そのクエリの AP である。

        :param DomainReidRankSequence ranking_sequence: クエリに対する類似度順のランキング
        :return DomainReidAp: 算出した AP
        """
        ap = 0.0
        if len(ranking_sequence) == 0:
            return cls(ap=0.0)
        for i, ranking in enumerate(ranking_sequence):
            ap += (i + 1) / ranking.rank
        return cls(ap=ap / len(ranking_sequence))
