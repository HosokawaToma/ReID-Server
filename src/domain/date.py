"""
日付のドメインモデル

年・月・日を保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DomainDate:
    """
    日付のドメインモデル
    :param int year: 年
    :param int month: 月
    :param int day: 日
    """
    year: int
    month: int
    day: int
