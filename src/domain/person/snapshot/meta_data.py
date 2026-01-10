from dataclasses import dataclass
import uuid
from datetime import datetime

@dataclass
class DomainPersonSnapshotMetaData:
    """
    人物写真のメタデータを表すドメイン知識を集約する
    :param uuid.UUID id: 人物写真のID
    :param int camera_id: カメラID
    :param int view_id: ビューID
    :param datetime timestamp: 撮影時刻
    :param bool is_junk: ゴミかどうか
    :param uuid.UUID | None person_id: 人物ID
    """
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    is_junk: bool
    person_id: uuid.UUID | None
