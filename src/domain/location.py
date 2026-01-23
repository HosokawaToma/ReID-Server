from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainLocation(DomainUtilsBase):
    """
    位置のドメインモデル
    """
    camera_id: int
    view_id: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DomainLocation):
            return False
        return self.camera_id == other.camera_id and self.view_id == other.view_id

    def __hash__(self) -> int:
        return hash((self.camera_id, self.view_id))
