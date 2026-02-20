"""
ReID CMC 曲線のドメインモデル

ランクごとの累積一致率のリストを保持する。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainReidCmcCurve(DomainUtilsBase):
    """
    ReID の CMC（Cumulative Matching Characteristics）曲線のドメインモデル。

    ランク 1 から順に、そのランクまでの累積一致率を並べたリストを保持する。長さは 50 を想定する。
    """
    cmc_curve: list[float]
