"""
タイムスタンプのドメインモデル

日時を保持し、その日の 0 時 0 分 0 秒・前日・翌日の 0 時 0 分 0 秒の取得、
秒数との加減算、Unix 秒・日付との相互変換、大小比較を提供する。
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
    """現在は未使用。共通のエラークラスを送出する運用のため、このクラスは送出されない。"""
    pass


class DomainTimestampSubError(Error):
    """現在は未使用。共通のエラークラスを送出する運用のため、このクラスは送出されない。"""
    pass


@dataclass(frozen=True)
class DomainTimestamp(DomainUtilsBase):
    """
    時刻のドメインモデル。

    日時を保持する。指定がなければ現在日時となる。
    Unix 秒（浮動小数点）から、または日付（その日の 0 時 0 分 0 秒）からも生成できる。
    秒数との加算・減算、別のタイムスタンプとの減算（結果は秒数）をサポートする。
    """
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_float(cls, timestamp: float) -> "DomainTimestamp":
        """
        Unix タイムスタンプ（秒、浮動小数点）から日時を生成する。

        ローカルタイムゾーンで解釈される。

        :param float timestamp: Unix 秒（UTC からの経過秒数）
        :return DomainTimestamp: 対応する日時を保持するインスタンス
        """
        return DomainTimestamp(
            timestamp=datetime.fromtimestamp(timestamp),
        )

    @classmethod
    def from_date(cls, date: DomainDate) -> "DomainTimestamp":
        """
        日付の 0 時 0 分 0 秒を表すタイムスタンプを生成する。

        時刻部分は 00:00:00 に固定される。

        :param DomainDate date: 年・月・日を表すドメイン日付
        :return DomainTimestamp: その日の 0 時 0 分 0 秒のインスタンス
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
        """秒数を加算した新しいタイムスタンプを返す。"""
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
        秒数を引いた場合は秒を減算したタイムスタンプを、別のタイムスタンプを引いた場合はその秒数差を返す。
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
        """比較対象がタイムスタンプまたは日付であり、日時が等しい場合に True を返す。"""
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
