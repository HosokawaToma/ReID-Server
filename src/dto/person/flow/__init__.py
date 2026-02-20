"""
人物フロー DTO

人物のカメラ間移動（ソース・ターゲットのカメラ・タイムスタンプ）を保持する。
"""
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass(frozen=True)
class DtoPersonFlow:
    """
    人物フロー（カメラ間移動）を保持する DTO。人物ID・ソース/ターゲットのカメラID・タイムスタンプを API で返す際に用いる。
    """
    person_id: uuid.UUID
    source_camera_id: int
    target_camera_id: int
    source_timestamp: datetime
    target_timestamp: datetime
