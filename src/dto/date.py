"""
日付 DTO

年・月・日を保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoDate:
    """
    日付を表すDTO
    :param int year: 年
    :param int month: 月
    :param int day: 日
    """
    year: int
    month: int
    day: int
