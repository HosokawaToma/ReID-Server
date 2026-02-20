"""
人物フロー重み検索クエリ DTO

タイムスタンプ範囲を保持する。
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DtoPersonFlowWeightQuery:
    """
    人物フロー重みクエリを表すDTO
    :param datetime timestamp_after: タイムスタンプ以降
    :param datetime timestamp_before: タイムスタンプ以前
    """
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
