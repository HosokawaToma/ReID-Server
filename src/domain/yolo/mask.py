from dataclasses import dataclass
import numpy as np
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainYoloMask(DomainUtilsBase):
    """
    YOLOのマスクのドメインモデル
    """
    mask: np.ndarray

    def __post_init__(self):
        """
        不変性を保つために、numpy.ndarrayを書き込み不可にする
        """
        self.mask.flags.writeable = False
