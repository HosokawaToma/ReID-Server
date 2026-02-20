"""
IDのドメインモデル

UUID をラップし、等価比較・ハッシュ・文字列化を提供する。
"""
from dataclasses import dataclass, field
import uuid
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainId(DomainUtilsBase):
    """
    IDのドメインモデル。

    UUID を保持し、未指定時は uuid4 で自動生成する。
    """
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __str__(self) -> str:
        """UUID の文字列表現を返す。"""
        return str(self.id)

    def __eq__(self, other: object) -> bool:
        """
        同一の UUID かどうかを返す。

        :param object other: 比較対象
        :return bool: 等しければ True
        """
        if not isinstance(other, DomainId):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """
        ハッシュ値を返す。セットや辞書のキーに用いる。

        :return int: ハッシュ値
        """
        return hash(self.id)
