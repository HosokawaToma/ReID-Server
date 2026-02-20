"""
人物フロー重み検索クエリ DTO

タイムスタンプ範囲を保持する。
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DtoPersonFlowWeightQuery:
    """
    人物フロー重み検索のクエリ条件を保持する DTO。

    タイムスタンプの範囲（以降・以前）を任意で指定できる。未指定の項目は検索条件に含めない。
    """
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
