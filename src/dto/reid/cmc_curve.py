"""
ReID CMC 曲線 DTO

ランクごとの累積一致率のリストを保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoReidCmcCurve:
    """
    ReID 評価の CMC 曲線（ランクごとの累積一致率のリスト）を保持する DTO。
    """
    cmc_curve: list[float]
