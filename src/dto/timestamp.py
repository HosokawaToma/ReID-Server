"""
タイムスタンプ DTO

日時を保持する。
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DtoTimestamp:
    """
    タイムスタンプを保持する DTO。

    日時を 1 つ保持する。API で撮影時刻などを渡すために用いる。

    :param datetime timestamp: 日時
    """
    timestamp: datetime
