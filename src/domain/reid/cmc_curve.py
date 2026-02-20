"""
ReID CMC 曲線のドメインモデル

ランクごとの累積一致率のリストを保持する。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainReidCmcCurve(DomainUtilsBase):
    """
    CMC曲線のドメインモデル
    """
    cmc_curve: list[float]
