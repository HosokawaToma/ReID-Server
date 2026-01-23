from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainYoloKeyPoint(DomainUtilsBase):
    """
    YOLOのキーポイントのドメインモデル
    """
    x: float
    y: float
    confidence: float
