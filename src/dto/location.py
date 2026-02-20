"""
位置 DTO

カメラID・ビューIDを保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoLocation:
    """
    撮影位置を保持する DTO。

    カメラID とビューID の組み合わせで、画像の撮影位置を表す。

    :param int camera_id: カメラID
    :param int view_id: ビューID
    """
    camera_id: int
    view_id: int
