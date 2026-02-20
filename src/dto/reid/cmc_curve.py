"""
ReID CMC 曲線 DTO

ランクごとの累積一致率のリストを保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoReidCmcCurve:
    """
    CMC曲線を表すDTO
    """
    cmc_curve: list[float]
