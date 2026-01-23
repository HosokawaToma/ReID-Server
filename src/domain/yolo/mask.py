from dataclasses import dataclass
import numpy as np
from domain.utils.base import DomainUtilsBase

@dataclass
class DomainYoloMask(DomainUtilsBase):
    """
    YOLOのマスクのドメインモデル
    """
    mask: np.ndarray
