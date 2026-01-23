from dataclasses import dataclass
import jwt
from domain.token import DomainToken
from domain.timestamp import DomainTimestamp
from domain.utils.base import DomainUtilsBase
from domain.client.id import DomainClientId
from domain.client.password import DomainClientPassword

@dataclass(frozen=True)
class DomainClientAuthCredentials(DomainUtilsBase):
    """
    クライアント認証資格情報を表すドメインモデル
    """
    id: DomainClientId
    password: DomainClientPassword

    def authenticate(self, id: DomainClientId, password: DomainClientPassword) -> bool:
        return self.id == id and self.password == password

    def generate_token(self, secret_key: str, algorithm: str, expire_minutes: int) -> DomainToken:
        return DomainToken(
            token=jwt.encode(
                {"id": str(self.id)},
                secret_key,
                algorithm=algorithm,
            ),
            expires_at=DomainTimestamp().from_now(expire_minutes * 60),
        )

    @classmethod
    def convert_token(cls, token: str, secret_key: str, algorithm: str) -> DomainClientId:
        return DomainClientId(id=jwt.decode(token, secret_key, algorithms=[algorithm])["id"])
