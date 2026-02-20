"""
位置のドメインモデル

カメラID・ビューIDを保持し、等価・ハッシュをサポートする。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainLocation(DomainUtilsBase):
    """
    位置のドメインモデル。

    カメラID とビューID の組み合わせで撮影位置を一意に識別する。等価比較とハッシュは両方の値に基づく。
    """
    camera_id: int
    view_id: int

    def __eq__(self, other: object) -> bool:
        """比較対象が同じ型かつカメラID・ビューID がともに一致する場合に True を返す。"""
        if not isinstance(other, DomainLocation):
            return False
        return self.camera_id == other.camera_id and self.view_id == other.view_id

    def __hash__(self) -> int:
        """カメラID とビューID に基づくハッシュを返す。セット・辞書のキーに利用できる。"""
        return hash((self.camera_id, self.view_id))
