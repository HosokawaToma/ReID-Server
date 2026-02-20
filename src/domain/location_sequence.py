"""
位置シーケンスのドメインモデル

位置（カメラ・ビュー）のリストを保持する。
"""
from dataclasses import dataclass
from domain.location import DomainLocation
from domain.utils.sequence_base import DomainUtilsSequenceBase


@dataclass(frozen=True)
class DomainLocationSequence(DomainUtilsSequenceBase[DomainLocation]):
    """位置のシーケンス。"""
    pass
