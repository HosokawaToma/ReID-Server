from dataclasses import dataclass
from domain.timestamp import DomainTimestamp
from domain.id import DomainId
from domain.location import DomainLocation

@dataclass
class DomainCameraFrame:
    """
    カメラフレームのドメインモデル
    """
    id: DomainId
    location: DomainLocation
    timestamp: DomainTimestamp
