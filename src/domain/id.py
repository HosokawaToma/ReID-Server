"""
ID のドメインモデル

エンティティやリソースを一意に識別するための UUID をラップし、等価比較・ハッシュ・
文字列化を提供する。指定がなければ uuid4 で自動採番する。
"""
from dataclasses import dataclass, field
import uuid
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainId(DomainUtilsBase):
    """
    ID のドメインモデル。

    カメラフレーム・人物スナップショットなど、各種エンティティの主キーとして用いる。
    UUID を保持する。指定がなければ uuid4 で採番する。不変であり、等価比較とハッシュによりセットや辞書のキーに利用できる。
    """
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __str__(self) -> str:
        """UUID の文字列表現（ハイフン付き標準形式）を返す。"""
        return str(self.id)

    def __eq__(self, other: object) -> bool:
        """
        比較対象が同じ型かつ保持する UUID が一致する場合に True を返す。

        :param object other: 比較対象
        :return bool: 同一 UUID なら True、型が違うか UUID が異なれば False
        """
        if not isinstance(other, DomainId):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """
        保持する UUID のハッシュを返す。不変かつ等価比較と整合するため、セット・辞書のキーに利用できる。

        :return int: ハッシュ値
        """
        return hash(self.id)
