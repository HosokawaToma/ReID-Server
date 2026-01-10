from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class DtoPersonFlow:
    """
    人物フローを表すDTO
    :param uuid.UUID person_id: 人物ID
    :param int source_camera_id: ソースカメラID
    :param int target_camera_id: ターゲットカメラID
    :param datetime source_timestamp: ソースタイムスタンプ
    :param datetime target_timestamp: ターゲットタイムスタンプ
    """
    person_id: uuid.UUID
    source_camera_id: int
    target_camera_id: int
    source_timestamp: datetime
    target_timestamp: datetime
