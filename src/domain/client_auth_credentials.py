from dataclasses import dataclass
import hashlib
import jwt
from domain.token import DomainToken
from domain.timestamp import DomainTimestamp
from domain.utils.base import DomainUtilsBase

@dataclass
class DomainClientAuthCredentials(DomainUtilsBase):
    """
    クライアント認証資格情報を表すドメインモデル
    """
    id: str
    password: str

    def authenticate(self, id: str, password: str) -> bool:
        return self.id == id and self.password == hashlib.sha256(password.encode()).hexdigest()

    def generate_token(self, secret_key: str, algorithm: str, expire_minutes: int) -> DomainToken:
        return DomainToken(
            token=jwt.encode(
                {"id": self.id},
                secret_key,
                algorithm=algorithm,
            ),
            expires_at=DomainTimestamp().from_now(expire_minutes * 60),
        )

    @classmethod
    def convert_token(cls, token: str, secret_key: str, algorithm: str) -> str:
        return jwt.decode(token, secret_key, algorithms=[algorithm])["id"]
