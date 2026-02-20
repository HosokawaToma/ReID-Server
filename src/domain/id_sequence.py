"""
ID のシーケンスのドメインモデル

識別子（UUID）のリストを保持するシーケンス。末尾追加・インデックス参照・長さ・結合などシーケンス基底の操作を利用できる。
"""
from dataclasses import dataclass
from domain.id import DomainId
from domain.utils.sequence_base import DomainUtilsSequenceBase


@dataclass(frozen=True)
class DomainIdSequence(DomainUtilsSequenceBase[DomainId]):
    """
    ID のシーケンスのドメインモデル。

    識別子のリストを保持する。シーケンス基底の末尾追加・インデックス参照・長さ取得・同型シーケンスとの結合が可能。
    """
    pass
