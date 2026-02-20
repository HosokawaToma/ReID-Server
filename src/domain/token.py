"""
トークンのドメインモデル

JWT のエンコード・デコードを提供する。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from typing import Any
import jwt


@dataclass(frozen=True)
class DomainToken(DomainUtilsBase):
    """
    トークンのドメインモデル。

    JWT 文字列を保持する。
    """
    token: str

    @classmethod
    def encode(cls, payload: dict[str, Any], secret_key: str, algorithm: str) -> "DomainToken":
        """
        ペイロードを JWT にエンコードして DomainToken を生成する。

        :param dict[str, Any] payload: ペイロード
        :param str secret_key: 秘密鍵
        :param str algorithm: アルゴリズム
        :return DomainToken: エンコード済みトークン
        """
        return DomainToken(
            token=jwt.encode(payload, secret_key, algorithm=algorithm),
        )

    def decode(self, secret_key: str, algorithm: str) -> dict[str, Any]:
        """
        JWT をデコードしてペイロードを返す。

        :param str secret_key: 秘密鍵
        :param str algorithm: アルゴリズム
        :return dict[str, Any]: ペイロード
        """
        decoded = jwt.decode(
            self.token,
            secret_key,
            algorithms=[algorithm],
        )
        return decoded
