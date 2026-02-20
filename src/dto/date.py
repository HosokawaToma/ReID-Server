"""
日付 DTO

年・月・日を保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoDate:
    """
    日付を保持する DTO。

    API のクエリやレスポンスで年・月・日を渡すために用いる。

    :param int year: 年
    :param int month: 月
    :param int day: 日
    """
    year: int
    month: int
    day: int
