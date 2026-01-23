from dataclasses import dataclass, InitVar, field
from domain.utils.base import DomainUtilsBase
import hashlib

@dataclass(frozen=True)
class DomainClientPassword(DomainUtilsBase):
    """
    クライアントパスワードを表すドメインモデル
    """
    hashed_password: str = field(init=False)
    password: InitVar[str]

    def __post_init__(self, password: str):
        object.__setattr__(self, "hashed_password", hashlib.sha256(password.encode()).hexdigest())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DomainClientPassword):
            return False
        return self.hashed_password == other.hashed_password

    def __hash__(self) -> int:
        return hash(self.hashed_password)

    def __str__(self) -> str:
        return self.hashed_password
