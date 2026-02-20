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

    カメラとビューの組み合わせで一意に識別する。
    """
    camera_id: int
    view_id: int

    def __eq__(self, other: object) -> bool:
        """camera_id と view_id が一致する場合に等しいとみなす。"""
        if not isinstance(other, DomainLocation):
            return False
        return self.camera_id == other.camera_id and self.view_id == other.view_id

    def __hash__(self) -> int:
        """camera_id と view_id のタプルでハッシュを返す。"""
        return hash((self.camera_id, self.view_id))
