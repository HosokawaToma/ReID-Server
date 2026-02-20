"""
人物スナップショット詳細のドメインモデル

ID・位置・タイムスタンプ・人物IDのみを保持する（画像・特徴量なし）。
"""
from dataclasses import dataclass
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.person.id import DomainPersonId
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainPersonSnapshotDetail(DomainUtilsBase):
    """
    人物スナップショットの詳細（メタデータのみ）を表す。
    """
    id: DomainId
    location: DomainLocation
    timestamp: DomainTimestamp
    person_id: DomainPersonId
