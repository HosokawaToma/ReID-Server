"""
人物スナップショット検索クエリ DTO

検索条件とソートキーを保持する。
"""
from dataclasses import dataclass
import uuid
from datetime import datetime

from enum import Enum


class DtoPersonSnapshotQuerySortByKey(str, Enum):
    """
    人物検出検索のソートキーを表す列挙。timestamp_asc / timestamp_desc を保持する。
    """
    TIMESTAMP_ASC = "timestamp_asc"
    TIMESTAMP_DESC = "timestamp_desc"


@dataclass(frozen=True)
class DtoPersonSnapshotQuery:
    """
    人物検出検索のクエリ条件を保持する DTO。

    ID・カメラ・ビュー・ゴミフラグ・人物ID・撮影時刻範囲・ソート順を任意で指定できる。未指定の項目は検索条件に含めない。
    """
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    is_junk: bool | None = None
    person_ids: list[uuid.UUID] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    sort_by_list: list[DtoPersonSnapshotQuerySortByKey] | None = None
