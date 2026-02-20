"""
YOLO バウンディングボックスのドメインモデル

検出框の座標・信頼度・クラスIDを保持する。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainYoloBoundingBox(DomainUtilsBase):
    """
    YOLOのバウンディングボックスのドメインモデル
    """
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    class_id: int
