from dataclasses import dataclass, field
from domain.id import DomainId
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainPersonId(DomainUtilsBase):
    """
    人物のIDのドメインモデル
    """
    id: DomainId | None = field(default=None)
    is_junk: bool = field(default=True)

    def new_id(self) -> "DomainPersonId":
        return DomainPersonId(id=DomainId(), is_junk=False)

    def junk(self) -> "DomainPersonId":
        return DomainPersonId(id=None, is_junk=True)

    def copy(self) -> "DomainPersonId":
        return DomainPersonId(id=self.id, is_junk=self.is_junk)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DomainPersonId):
            return False
        return self.id == other.id and self.is_junk == other.is_junk

    def __hash__(self) -> int:
        return hash((self.id, self.is_junk))
