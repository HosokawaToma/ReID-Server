from dataclasses import dataclass, field
from datetime import datetime
from datetime import timedelta
from typing import overload
from domain.utils.base import DomainUtilsBase
from domain.time import DomainTime
from domain.date import DomainDate
from error import Error

class DomainTimestampAddError(Error):
    pass

class DomainTimestampSubError(Error):
    pass

@dataclass(frozen=True)
class DomainTimestamp(DomainUtilsBase):
    """
    時刻のドメインモデル
    """
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_float(cls, timestamp: float) -> "DomainTimestamp":
        return DomainTimestamp(
            timestamp=datetime.fromtimestamp(timestamp),
        )

    @classmethod
    def from_date(cls, date: DomainDate) -> "DomainTimestamp":
        return DomainTimestamp(
            timestamp=datetime.combine(datetime(date.year, date.month, date.day), datetime.min.time()),
        )

    def today(self) -> "DomainTimestamp":
        return DomainTimestamp(
            timestamp=datetime.combine(self.timestamp.date(), datetime.min.time()),
        )

    def yesterday(self) -> "DomainTimestamp":
        return DomainTimestamp(
            timestamp=datetime.combine(self.timestamp.date() - timedelta(days=1), datetime.min.time()),
        )

    def tomorrow(self) -> "DomainTimestamp":
        return DomainTimestamp(
            timestamp=datetime.combine(self.timestamp.date() + timedelta(days=1), datetime.min.time()),
        )

    def __add__(self, other: "DomainTime") -> "DomainTimestamp":
        return DomainTimestamp(
            timestamp=self.timestamp + timedelta(seconds=other.seconds),
        )

    @overload
    def __sub__(self, other: DomainTime) -> "DomainTimestamp":
        pass

    @overload
    def __sub__(self, other: "DomainTimestamp") -> DomainTime:
        pass

    def __sub__(self, other: "DomainTime | DomainTimestamp") -> "DomainTimestamp | DomainTime":
        if isinstance(other, DomainTime):
            return DomainTimestamp(
                timestamp=self.timestamp - timedelta(seconds=other.seconds),
            )
        elif isinstance(other, DomainTimestamp):
            return DomainTime(
                seconds=self.timestamp.timestamp() - other.timestamp.timestamp(),
            )
        else:
            raise ValueError("other must be DomainTime or DomainTimestamp")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (DomainTimestamp, DomainDate)):
            return False
        if isinstance(other, DomainTimestamp):
            return self.timestamp == other.timestamp
        return self.timestamp.date() == DomainTimestamp.from_date(other).timestamp.date()

    def __lt__(self, other: "DomainTimestamp") -> bool:
        return self.timestamp < other.timestamp

    def __le__(self, other: "DomainTimestamp") -> bool:
        return self.timestamp <= other.timestamp

    def __gt__(self, other: "DomainTimestamp") -> bool:
        return self.timestamp > other.timestamp

    def __ge__(self, other: "DomainTimestamp") -> bool:
        return self.timestamp >= other.timestamp

    def __hash__(self) -> int:
        return hash(self.timestamp)

    def __str__(self) -> str:
        return self.timestamp.isoformat()

    def __float__(self) -> float:
        return float(self.timestamp.timestamp())
