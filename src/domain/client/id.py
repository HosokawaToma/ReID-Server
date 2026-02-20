"""
クライアントIDのドメインモデル

認証用のクライアント識別子を保持する。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainClientId(DomainUtilsBase):
    """
    認証用のクライアント識別子（文字列）を保持するドメインモデル。
    """
    id: str

    def __eq__(self, other: object) -> bool:
        """ID 文字列が一致する場合に等しいとみなす。"""
        if not isinstance(other, DomainClientId):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """ID のハッシュを返す。"""
        return hash(self.id)

    def __str__(self) -> str:
        """ID 文字列を返す。"""
        return self.id
