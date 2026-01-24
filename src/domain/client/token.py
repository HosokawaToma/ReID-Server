from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from domain.client.id import DomainClientId
from domain.timestamp import DomainTimestamp
from domain.token import DomainToken
from error import AuthenticationError

@dataclass(frozen=True)
class DomainClientToken(DomainUtilsBase):
    """
    クライアントトークンを表すドメインモデル
    """
    client_id: DomainClientId
    expires_at: DomainTimestamp

    @classmethod
    def decode(cls, token: DomainToken, secret_key: str, algorithm: str) -> "DomainClientToken":
        try:
            decoded = token.decode(secret_key, algorithm)
        except Exception as e:
            raise AuthenticationError("クライアントトークンが不正です")
        if not isinstance(decoded["id"], str):
            raise AuthenticationError("id must be a string")
        if not isinstance(decoded["exp"], float):
            raise AuthenticationError("exp must be a float")
        client_id = DomainClientId(id=decoded["id"])
        expires_at = DomainTimestamp.from_float(decoded["exp"])
        return DomainClientToken(client_id=client_id, expires_at=expires_at)

    def is_expired(self) -> bool:
        return self.expires_at < DomainTimestamp()
