from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainReidCmcCurve(DomainUtilsBase):
    """
    CMC曲線のドメインモデル
    """
    cmc_curve: list[float]
