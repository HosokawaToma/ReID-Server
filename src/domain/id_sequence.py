"""
IDのシーケンスのドメインモデル

DomainId のリストを保持するシーケンス。
"""
from dataclasses import dataclass
from domain.id import DomainId
from domain.utils.sequence_base import DomainUtilsSequenceBase


@dataclass(frozen=True)
class DomainIdSequence(DomainUtilsSequenceBase[DomainId]):
    """
    IDのシーケンスのドメインモデル。

    DomainId のリストを保持し、シーケンス基底の操作を提供する。
    """
    pass
