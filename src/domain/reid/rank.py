"""
ReID ランクのドメインモデル

検出結果 ID とランク順位を保持する。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from domain.id import DomainId


@dataclass(frozen=True)
class DomainReidRank(DomainUtilsBase):
    """
    ReID 評価におけるランクのドメインモデル。

    クエリに対して類似度順に並んだとき、正解の人物検出結果が何番目に現れるかを表す。1 位なら 1、2 位なら 2。

    :param DomainId id: 人物検出結果の識別子
    :param int rank: ランク（1 始まり）
    """
    id: DomainId
    rank: int
