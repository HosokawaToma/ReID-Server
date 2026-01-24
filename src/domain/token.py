from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from typing import Any
import jwt

@dataclass(frozen=True)
class DomainToken(DomainUtilsBase):
    """
    トークンのドメインモデル
    """
    token: str

    @classmethod
    def encode(cls, payload: dict[str, Any], secret_key: str, algorithm: str) -> "DomainToken":
        return DomainToken(
            token=jwt.encode(payload, secret_key, algorithm=algorithm),
        )

    def decode(self, secret_key: str, algorithm: str) -> dict[str, Any]:
        decoded = jwt.decode(
            self.token,
            secret_key,
            algorithms=[algorithm],
        )
        return decoded
