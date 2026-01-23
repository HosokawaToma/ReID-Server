from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainTime(DomainUtilsBase):
    """
    時刻のドメインモデル
    """
    seconds: float

    def __add__(self, other: "DomainTime") -> "DomainTime":
        return DomainTime(
            seconds=self.seconds + other.seconds,
        )

    def __sub__(self, other: "DomainTime") -> "DomainTime":
        return DomainTime(
            seconds=self.seconds - other.seconds,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DomainTime):
            return False
        return self.seconds == other.seconds

    def __lt__(self, other: "DomainTime") -> bool:
        return self.seconds < other.seconds

    def __le__(self, other: "DomainTime") -> bool:
        return self.seconds <= other.seconds

    def __gt__(self, other: "DomainTime") -> bool:
        return self.seconds > other.seconds

    def __ge__(self, other: "DomainTime") -> bool:
        return self.seconds >= other.seconds

    def __hash__(self) -> int:
        return hash(self.seconds)

    def __str__(self) -> str:
        return str(self.seconds)
