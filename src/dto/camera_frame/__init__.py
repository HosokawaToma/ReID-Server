"""
カメラフレーム DTO

フレームの ID・位置・タイムスタンプを保持する。
"""
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass(frozen=True)
class DtoCameraFrame:
    """
    カメラフレームを表す DTO。

    :param uuid.UUID id: フレームID
    :param int camera_id: カメラID
    :param int view_id: ビューID
    :param datetime timestamp: タイムスタンプ
    """
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
