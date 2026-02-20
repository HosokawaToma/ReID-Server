"""
人物スナップショット詳細 DTO

ID・位置・タイムスタンプ・ゴミフラグ・人物ID を保持する。
"""
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass(frozen=True)
class DtoPersonSnapshotDetail:
    """
    人物写真の詳細を表すDTO。
    """
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    is_junk: bool
    person_id: uuid.UUID | None
