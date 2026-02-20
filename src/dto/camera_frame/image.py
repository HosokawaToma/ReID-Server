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
    カメラフレーム画像を表す DTO。

    :param uuid.UUID id: フレームID
    :param int camera_id: カメラID
    :param int view_id: ビューID
    :param datetime timestamp: タイムスタンプ
    :param Image.Image image: PIL 画像
    :param str format: 画像フォーマット
    """
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    image: Image.Image
    format: str
