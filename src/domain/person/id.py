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

    def new_id(self) -> None:
        self = DomainPersonId(id=DomainId(), is_junk=False)

    def set_id(self, other: "DomainPersonId") -> None:
        self = DomainPersonId(id=other.id, is_junk=other.is_junk)

    def junk(self) -> None:
        self = DomainPersonId(id=None, is_junk=True)
