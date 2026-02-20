"""
クライアント認証資格情報のドメインモデル

ID・パスワードの照合と JWT 発行を提供する。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from domain.client.id import DomainClientId
from domain.client.password import DomainClientPassword
from domain.token import DomainToken
from domain.timestamp import DomainTimestamp
from domain.time import DomainTime


@dataclass(frozen=True)
class DomainClientAuthCredentials(DomainUtilsBase):
    """
    クライアント認証用の資格情報（ID・パスワード）を保持するドメインモデル。照合と JWT 発行を提供する。
    """
    id: DomainClientId
    password: DomainClientPassword

    def authenticate(self, id: DomainClientId, password: DomainClientPassword) -> bool:
        """
        クライアント認証資格情報を認証する
        :param DomainClientId id: クライアントID
        :param DomainClientPassword password: クライアントパスワード
        :return bool: 認証結果
        """
        return self.id == id and self.password == password

    def to_token(self, secret_key: str, algorithm: str, expire_minutes: int) -> DomainToken:
        """
        資格情報から有効期限付き JWT を発行する。

        :param str secret_key: 秘密鍵
        :param str algorithm: アルゴリズム
        :param int expire_minutes: 有効分数
        :return DomainToken: JWT
        """
        return DomainToken.encode(
            payload={
                "id": str(self.id),
                "exp": float(DomainTimestamp() + DomainTime(seconds=expire_minutes * 60)),
            },
            secret_key=secret_key,
            algorithm=algorithm,
        )
