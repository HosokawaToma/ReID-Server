"""
YOLO マスクのドメインモデル

セグメンテーション用の numpy 配列を保持する（不変化）。
"""
from dataclasses import dataclass, InitVar, field
import numpy as np
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainYoloMask(DomainUtilsBase):
    """
    YOLOのマスクのドメインモデル
    """
    mask: InitVar[np.ndarray]
    _mask: np.ndarray = field(init=False)

    def __post_init__(self, mask: np.ndarray):
        """
        不変性を保つために、numpy.ndarrayを書き込み不可にする
        """
        cloned_mask = mask.copy()
        cloned_mask.flags.writeable = False
        object.__setattr__(self, "_mask", cloned_mask)
