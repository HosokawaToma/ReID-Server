"""
YOLO バウンディングボックスのドメインモデル

検出框の座標・信頼度・クラスIDを保持する。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainYoloBoundingBox(DomainUtilsBase):
    """
    YOLO のバウンディングボックスのドメインモデル。

    検出框の左上・右下の座標、信頼度（0～1）、クラスID を保持する。人物検出ではクラス 0 を想定する。
    """
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    class_id: int
