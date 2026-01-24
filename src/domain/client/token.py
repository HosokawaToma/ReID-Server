from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from domain.client.id import DomainClientId
from domain.timestamp import DomainTimestamp
from domain.token import DomainToken

@dataclass(frozen=True)
class DomainClientToken(DomainUtilsBase):
    """
    クライアントトークンを表すドメインモデル
    """
    client_id: DomainClientId
    expires_at: DomainTimestamp

    @classmethod
    def decode(cls, token: DomainToken, secret_key: str, algorithm: str) -> "DomainClientToken":
        decoded = token.decode(secret_key, algorithm)
        if not isinstance(decoded["id"], str):
            raise ValueError("id must be a string")
        if not isinstance(decoded["exp"], float):
            raise ValueError("exp must be a float")
        client_id = DomainClientId(id=decoded["id"])
        expires_at = DomainTimestamp.from_float(decoded["exp"])
        return DomainClientToken(client_id=client_id, expires_at=expires_at)

    def is_expired(self) -> bool:
        return self.expires_at < DomainTimestamp()
