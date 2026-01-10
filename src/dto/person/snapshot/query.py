from dataclasses import dataclass
import uuid
from datetime import datetime

from enum import Enum
class DtoPersonSnapshotQuerySortByKey(str, Enum):
    TIMESTAMP_ASC = "timestamp_asc"
    TIMESTAMP_DESC = "timestamp_desc"

@dataclass
class DtoPersonSnapshotQuery:
    """
    人物写真クエリを表すDTO
    :param list[uuid.UUID] ids: 人物写真IDリスト
    :param list[int] camera_ids: カメラIDリスト
    :param list[int] view_ids: ビューIDリスト
    :param bool is_junk: ゴミかどうか
    :param list[uuid.UUID] person_ids: 人物IDリスト
    :param datetime timestamp_after: 撮影時刻以降
    :param datetime timestamp_before: 撮影時刻以前
    """
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    is_junk: bool | None = None
    person_ids: list[uuid.UUID] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    sort_by_list: list[DtoPersonSnapshotQuerySortByKey] | None = None
