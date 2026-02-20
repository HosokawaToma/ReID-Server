"""
日付のドメインモデル

年・月・日を保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DomainDate:
    """
    日付のドメインモデル。

    年・月・日を整数で保持する。タイムスタンプの「その日の 0 時 0 分 0 秒」の生成などに用いる。

    :param int year: 年
    :param int month: 月
    :param int day: 日
    """
    year: int
    month: int
    day: int
