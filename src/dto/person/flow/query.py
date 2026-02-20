"""
人物フロー検索クエリ DTO

人物ID とタイムスタンプ範囲を保持する。
"""
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass(frozen=True)
class DtoPersonFlowQuery:
    """
    人物フロー検索のクエリ条件を保持する DTO。人物ID・タイムスタンプ範囲を任意で指定できる。
    """
    person_id: uuid.UUID
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
