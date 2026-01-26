from dataclasses import dataclass
import uuid

from enum import Enum
class DtoPersonSnapshotAnswerQuerySortByKey(str, Enum):
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"

@dataclass(frozen=True)
class DtoPersonSnapshotAnswerQuery:
    """
    人物検出結果の正解ラベルクエリを表すDTO
    :param list[uuid.UUID] person_snapshot_ids: 人物検出結果IDリスト
    :param list[uuid.UUID] person_ids: 人物IDリスト
    :param bool is_junk: ゴミかどうか
    :param list[DtoPersonSnapshotAnswerQuerySortByKey] sort_by_list: ソートキーリスト
    """
    person_snapshot_ids: list[uuid.UUID] | None = None
    person_ids: list[uuid.UUID] | None = None
    is_junk: bool | None = None
    sort_by_list: list[DtoPersonSnapshotAnswerQuerySortByKey] | None = None
