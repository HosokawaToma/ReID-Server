"""
人物スナップショットと人物IDの対応 DTO

検出結果ID・人物ID・ゴミフラグを保持する。
"""
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class DtoPersonSnapshotPersonId:
    """
    人物検出結果と人物IDの対応（正解ラベル）を保持する DTO。

    検出結果ID・人物ID・ゴミフラグを API で受け渡す際に用いる。
    """
    id: uuid.UUID
    person_id: uuid.UUID | None
    is_junk: bool
