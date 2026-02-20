"""
タイムスタンプのドメインモデル

日時を保持し、日付変換・加減算・比較を提供する。
"""
from dataclasses import dataclass, field
from datetime import datetime
from datetime import timedelta
from typing import overload
from domain.utils.base import DomainUtilsBase
from domain.time import DomainTime
from domain.date import DomainDate
from error import Error


class DomainTimestampAddError(Error):
    """時刻の加算で発生するエラー。"""
    pass


class DomainTimestampSubError(Error):
    """時刻の減算で発生するエラー。"""
    pass


@dataclass(frozen=True)
class DomainTimestamp(DomainUtilsBase):
    """
    時刻のドメインモデル
    """
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_float(cls, timestamp: float) -> "DomainTimestamp":
        """
        Unix タイムスタンプから DomainTimestamp を生成する。

        :param float timestamp: Unix 秒
        :return DomainTimestamp: タイムスタンプ
        """
        return DomainTimestamp(
            timestamp=datetime.fromtimestamp(timestamp),
        )

    @classmethod
    def from_date(cls, date: DomainDate) -> "DomainTimestamp":
        """
        日付の 0 時 0 分 0 秒の DomainTimestamp を生成する。

        :param DomainDate date: 日付
        :return DomainTimestamp: タイムスタンプ
        """
        return DomainTimestamp(
            timestamp=datetime.combine(
                datetime(date.year, date.month, date.day), datetime.min.time()),
        )

    def today(self) -> "DomainTimestamp":
        """このタイムスタンプの日付の 0 時 0 分 0 秒を返す。"""
        return DomainTimestamp(
            timestamp=datetime.combine(
                self.timestamp.date(), datetime.min.time()),
        )

    def yesterday(self) -> "DomainTimestamp":
        """前日の 0 時 0 分 0 秒を返す。"""
        return DomainTimestamp(
            timestamp=datetime.combine(
                self.timestamp.date() - timedelta(days=1), datetime.min.time()),
        )

    def tomorrow(self) -> "DomainTimestamp":
        """翌日の 0 時 0 分 0 秒を返す。"""
        return DomainTimestamp(
            timestamp=datetime.combine(
                self.timestamp.date() + timedelta(days=1), datetime.min.time()),
        )

    def __add__(self, other: "DomainTime") -> "DomainTimestamp":
        """秒数を加算した新しい DomainTimestamp を返す。"""
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
        """
        DomainTime の場合は秒を減算した DomainTimestamp、DomainTimestamp の場合は差の DomainTime を返す。
        """
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
        """DomainTimestamp または DomainDate と日時が等しいかどうかを返す。"""
        if not isinstance(other, (DomainTimestamp, DomainDate)):
            return False
        if isinstance(other, DomainTimestamp):
            return self.timestamp == other.timestamp
        return self.timestamp.date() == DomainTimestamp.from_date(other).timestamp.date()

    def __lt__(self, other: "DomainTimestamp") -> bool:
        """日時の未満比較。"""
        return self.timestamp < other.timestamp

    def __le__(self, other: "DomainTimestamp") -> bool:
        """日時の以下比較。"""
        return self.timestamp <= other.timestamp

    def __gt__(self, other: "DomainTimestamp") -> bool:
        """日時の超過比較。"""
        return self.timestamp > other.timestamp

    def __ge__(self, other: "DomainTimestamp") -> bool:
        """日時の以上比較。"""
        return self.timestamp >= other.timestamp

    def __hash__(self) -> int:
        """日時のハッシュを返す。"""
        return hash(self.timestamp)

    def __str__(self) -> str:
        """ISO 形式の文字列を返す。"""
        return self.timestamp.isoformat()

    def __float__(self) -> float:
        """Unix タイムスタンプ（秒）を返す。"""
        return float(self.timestamp.timestamp())
