"""
ReID mAP DTO

平均精度の平均値を保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoReidMap:
    """
    mAPのDTO
    """
    map: float
