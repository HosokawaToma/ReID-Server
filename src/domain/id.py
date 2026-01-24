from dataclasses import dataclass, field
import uuid
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainId(DomainUtilsBase):
    """
    IDのドメインモデル
    """
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __str__(self) -> str:
        return str(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DomainId):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
