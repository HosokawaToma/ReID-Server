from dataclasses import dataclass, field, InitVar
from domain.utils.base import DomainUtilsBase
from datetime import timedelta

@dataclass(frozen=True)
class DomainTime(DomainUtilsBase):
    """
    時刻のドメインモデル
    """
    time: timedelta = field(init=False)
    total_seconds: InitVar[float]

    def __post_init__(self, total_seconds: float):
        object.__setattr__(self, "time", timedelta(seconds=total_seconds))

    def __add__(self, other: "DomainTime") -> "DomainTime":
        return DomainTime(
            total_seconds=self.time.total_seconds() + other.time.total_seconds(),
        )

    def __sub__(self, other: "DomainTime") -> "DomainTime":
        return DomainTime(
            total_seconds=self.time.total_seconds() - other.time.total_seconds(),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DomainTime):
            return False
        return self.time == other.time

    def __lt__(self, other: "DomainTime") -> bool:
        return self.time < other.time

    def __le__(self, other: "DomainTime") -> bool:
        return self.time <= other.time

    def __gt__(self, other: "DomainTime") -> bool:
        return self.time > other.time

    def __ge__(self, other: "DomainTime") -> bool:
        return self.time >= other.time

    def __hash__(self) -> int:
        return hash(self.time)

    def __str__(self) -> str:
        return str(self.time)
