"""
タイムスタンプ DTO

日時を保持する。
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DtoTimestamp:
    """
    タイムスタンプを表す DTO。

    :param datetime timestamp: 日時
    """
    timestamp: datetime
