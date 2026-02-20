"""
クライアントトークンのドメインモデル

JWT からクライアントIDと有効期限を復元し、期限切れ判定を提供する。
"""
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
        """
        JWT をデコードしてクライアントトークンを生成する。

        :param DomainToken token: JWT
        :param str secret_key: 秘密鍵
        :param str algorithm: アルゴリズム
        :return DomainClientToken: クライアントトークン
        :raises AuthenticationError: トークンが不正な場合
        """
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
        """
        現在時刻が有効期限を過ぎているかどうかを返す。

        :return bool: 期限切れなら True
        """
        return self.expires_at < DomainTimestamp()
