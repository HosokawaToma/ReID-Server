"""
人物フローのドメインモデル

人物のカメラ間移動（ソース・ターゲットの位置・タイムスタンプ）を保持する。
"""
from dataclasses import dataclass
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.id import DomainId
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainPersonFlow(DomainUtilsBase):
    """
    個人の移動のドメインモデル
    """
    person_id: DomainId
    source_location: DomainLocation
    target_location: DomainLocation
    source_timestamp: DomainTimestamp
    target_timestamp: DomainTimestamp
