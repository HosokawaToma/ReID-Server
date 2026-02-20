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
    カメラフレームを保持する DTO。

    フレームの識別子・カメラID・ビューID・タイムスタンプを API で受け渡す際に用いる。
    """
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
