from dataclasses import dataclass
from datetime import datetime

@dataclass
class DtoFrameImageProperty:
    """
    フレーム画像のプロパティを表すDTO
    :param int camera_id: カメラID
    :param int view_id: ビューID
    :param datetime timestamp: タイムスタンプ
    """
    camera_id: int
    view_id: int
    timestamp: datetime
