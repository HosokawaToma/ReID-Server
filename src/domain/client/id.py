from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainClientId(DomainUtilsBase):
    """
    クライアントIDを表すドメインモデル
    """
    id: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DomainClientId):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return self.id
