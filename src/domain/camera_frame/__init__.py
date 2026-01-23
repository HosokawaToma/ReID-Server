from dataclasses import dataclass
from domain.timestamp import DomainTimestamp
from domain.id import DomainId
from domain.location import DomainLocation
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainCameraFrame(DomainUtilsBase):
    """
    カメラフレームのドメインモデル
    """
    id: DomainId
    location: DomainLocation
    timestamp: DomainTimestamp
