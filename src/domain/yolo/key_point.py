"""
YOLO キーポイントのドメインモデル

座標と信頼度を保持する。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainYoloKeyPoint(DomainUtilsBase):
    """
    YOLO のキーポイントのドメインモデル。

    姿勢推定で得た 1 点の画像座標（X, Y）と信頼度を保持する。
    """
    x: float
    y: float
    confidence: float
