"""
人物スナップショットと人物IDの対応 DTO

検出結果ID・人物ID・ゴミフラグを保持する。
"""
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class DtoPersonSnapshotPersonId:
    """
    人物スナップショットと人物IDの対応を表す DTO。

    :param uuid.UUID id: スナップショットID
    :param uuid.UUID | None person_id: 人物ID（ゴミの場合は None）
    :param bool is_junk: ゴミデータかどうか
    """
    id: uuid.UUID
    person_id: uuid.UUID | None
    is_junk: bool
