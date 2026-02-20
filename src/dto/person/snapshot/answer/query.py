"""
人物スナップショット正解ラベル検索クエリ DTO

正解ラベル検索条件とソートキーを保持する。
"""
from dataclasses import dataclass
import uuid

from enum import Enum


class DtoPersonSnapshotAnswerQuerySortByKey(str, Enum):
    """正解ラベル検索のソートキー。"""
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"


@dataclass(frozen=True)
class DtoPersonSnapshotAnswerQuery:
    """
    人物検出結果の正解ラベル検索のクエリ条件を保持する DTO。

    人物検出ID・人物ID・ゴミフラグ・ソート順を任意で指定できる。未指定の項目は検索条件に含めない。
    """
    person_snapshot_ids: list[uuid.UUID] | None = None
    person_ids: list[uuid.UUID] | None = None
    is_junk: bool | None = None
    sort_by_list: list[DtoPersonSnapshotAnswerQuerySortByKey] | None = None
