from dataclasses import dataclass, field
from datetime import datetime
from datetime import timedelta
from domain.utils.base import DomainUtilsBase

@dataclass
class DomainTimestamp(DomainUtilsBase):
    """
    時刻のドメインモデル
    """
    timestamp: datetime = field(default_factory=datetime.now)

    def from_now(self, seconds: int) -> "DomainTimestamp":
        return DomainTimestamp(
            timestamp=self.timestamp + timedelta(seconds=seconds),
        )

    def today(self) -> "DomainTimestamp":
        return DomainTimestamp(
            timestamp=datetime.combine(self.timestamp.date(), datetime.min.time()),
        )

    def __sub__(self, other: "DomainTimestamp") -> timedelta:
        return self.timestamp - other.timestamp

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DomainTimestamp):
            return False
        return self.timestamp == other.timestamp

    def __lt__(self, other: "DomainTimestamp") -> bool:
        return self.timestamp < other.timestamp

    def __le__(self, other: "DomainTimestamp") -> bool:
        return self.timestamp <= other.timestamp

    def __gt__(self, other: "DomainTimestamp") -> bool:
        return self.timestamp > other.timestamp

    def __ge__(self, other: "DomainTimestamp") -> bool:
        return self.timestamp >= other.timestamp
