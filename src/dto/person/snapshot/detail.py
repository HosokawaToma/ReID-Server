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
    API で返す人物検出結果の詳細を保持する DTO。

    識別子・カメラID・ビューID・撮影時刻・ゴミフラグ・人物ID（未割当時は None）を含む。
    """
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    is_junk: bool
    person_id: uuid.UUID | None
