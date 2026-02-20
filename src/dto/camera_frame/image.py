"""
カメラフレーム画像 DTO

フレームのメタデータと PIL 画像・フォーマットを保持する。
"""
from dataclasses import dataclass
from datetime import datetime
import uuid
from PIL import Image


@dataclass(frozen=True)
class DtoCameraFrameImage:
    """
    カメラフレーム画像を保持する DTO。

    フレームのメタデータ（ID・カメラ・ビュー・タイムスタンプ）と PIL 画像・フォーマットを API で受け渡す際に用いる。
    """
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    image: Image.Image
    format: str
