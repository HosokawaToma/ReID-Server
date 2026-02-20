"""
時刻のドメインモデル

秒単位で保持し、加算・減算・比較をサポートする。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainTime(DomainUtilsBase):
    """
    時刻のドメインモデル。

    秒（float）で保持する。
    """
    seconds: float

    def __add__(self, other: "DomainTime") -> "DomainTime":
        """秒を加算した新しい DomainTime を返す。"""
        return DomainTime(
            seconds=self.seconds + other.seconds,
        )

    def __sub__(self, other: "DomainTime") -> "DomainTime":
        """秒を減算した新しい DomainTime を返す。"""
        return DomainTime(
            seconds=self.seconds - other.seconds,
        )

    def __eq__(self, other: object) -> bool:
        """秒が一致する場合に等しいとみなす。"""
        if not isinstance(other, DomainTime):
            return False
        return self.seconds == other.seconds

    def __lt__(self, other: "DomainTime") -> bool:
        """秒の大小で未満比較する。"""
        return self.seconds < other.seconds

    def __le__(self, other: "DomainTime") -> bool:
        """秒の大小で以下比較する。"""
        return self.seconds <= other.seconds

    def __gt__(self, other: "DomainTime") -> bool:
        """秒の大小で超過比較する。"""
        return self.seconds > other.seconds

    def __ge__(self, other: "DomainTime") -> bool:
        """秒の大小で以上比較する。"""
        return self.seconds >= other.seconds

    def __hash__(self) -> int:
        """秒のハッシュを返す。"""
        return hash(self.seconds)

    def __str__(self) -> str:
        """秒の文字列表現を返す。"""
        return str(self.seconds)
