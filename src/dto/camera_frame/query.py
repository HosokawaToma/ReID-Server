"""
カメラフレーム検索クエリ DTO

検索条件とソートキーを保持する。
"""
from dataclasses import dataclass
from datetime import datetime
import uuid
from enum import Enum


class DtoCameraFrameQuerySortByKey(str, Enum):
    """カメラフレーム検索のソートキー。"""
    TIMESTAMP_ASC = "timestamp_asc"
    TIMESTAMP_DESC = "timestamp_desc"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class DtoCameraFrameQuery:
    """
    カメラフレーム検索条件を表す DTO。
    """
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    sort_by_list: list[DtoCameraFrameQuerySortByKey] | None = None
