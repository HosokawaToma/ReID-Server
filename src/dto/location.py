"""
位置 DTO

カメラID・ビューIDを保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoLocation:
    """
    撮影位置を表す DTO。

    :param int camera_id: カメラID
    :param int view_id: ビューID
    """
    camera_id: int
    view_id: int
