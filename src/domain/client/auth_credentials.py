from dataclasses import dataclass
import jwt
from domain.token import DomainToken
from domain.timestamp import DomainTimestamp
from domain.utils.base import DomainUtilsBase
from domain.client.id import DomainClientId
from domain.client.password import DomainClientPassword
from domain.time import DomainTime

@dataclass(frozen=True)
class DomainClientAuthCredentials(DomainUtilsBase):
    """
    クライアント認証資格情報を表すドメインモデル
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

    def generate_token(self, secret_key: str, algorithm: str, expire_minutes: int) -> DomainToken:
        """
        クライアント認証資格情報からトークンを生成する
        :param str secret_key: シークレットキー
        :param str algorithm: アルゴリズム
        :param int expire_minutes: トークンの有効期限（分）
        :return DomainToken: トークン
        """
        return DomainToken(
            token=jwt.encode(
                {"id": str(self.id)},
                secret_key,
                algorithm=algorithm,
            ),
            expires_at=DomainTimestamp() + DomainTime(seconds=expire_minutes * 60),
        )

    @classmethod
    def convert_token(cls, token: str, secret_key: str, algorithm: str) -> DomainClientId:
        """
        トークンからクライアントIDを取得する
        :param str token: トークン
        :param str secret_key: シークレットキー
        :param str algorithm: アルゴリズム
        :return DomainClientId: クライアントID
        """
        return DomainClientId(id=jwt.decode(token, secret_key, algorithms=[algorithm])["id"])
