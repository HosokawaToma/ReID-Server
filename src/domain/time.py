from dataclasses import dataclass, field, InitVar
from domain.utils.base import DomainUtilsBase
from datetime import timedelta

@dataclass(frozen=True)
class DomainTime(DomainUtilsBase):
    """
    時刻のドメインモデル
    """
    time: timedelta = field(init=False)
    hours: InitVar[int] = 0
    minutes: InitVar[int] = 0
    seconds: InitVar[int] = 0

    def __post_init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        object.__setattr__(self, "time", timedelta(hours=hours, minutes=minutes, seconds=seconds))

    def __add__(self, other: "DomainTime") -> "DomainTime":
        self = DomainTime(
            seconds=self.time.seconds + other.time.seconds,
        )
        return self

    def __sub__(self, other: "DomainTime") -> "DomainTime":
        self = DomainTime(
            seconds=self.time.seconds - other.time.seconds,
        )
        return self

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
