"""
クライアントパスワードのドメインモデル

SHA-256 ハッシュ化したパスワードを保持する。
"""
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
        """
        ToDo: SHA-256ではブルートフォース攻撃に対して脆弱です。
        ToDo: ソルトを使用していないためレインボーテーブル攻撃に対して脆弱です。
        :param str password: パスワード
        """
        object.__setattr__(self, "hashed_password",
                           hashlib.sha256(password.encode()).hexdigest())

    def __eq__(self, other: object) -> bool:
        """ハッシュ済みパスワードが一致する場合に等しいとみなす。"""
        if not isinstance(other, DomainClientPassword):
            return False
        return self.hashed_password == other.hashed_password

    def __hash__(self) -> int:
        """ハッシュ済みパスワードのハッシュを返す。"""
        return hash(self.hashed_password)

    def __str__(self) -> str:
        """ハッシュ済みパスワード文字列を返す。"""
        return self.hashed_password
