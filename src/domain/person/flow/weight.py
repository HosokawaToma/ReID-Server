from dataclasses import dataclass
from domain.location import DomainLocation
from domain.utils.base import DomainUtilsBase

@dataclass
class DomainPersonFlowWeight(DomainUtilsBase):
    """
    個人の移動重みのドメインモデル
    """
    source_location: DomainLocation
    target_location: DomainLocation
    weight: int
