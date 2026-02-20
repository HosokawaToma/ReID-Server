"""
人物スナップショットのドメインモデル

検出結果の ID・位置・タイムスタンプ・画像・人物ID・特徴量・正解ラベルを保持する。
"""
from dataclasses import dataclass
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.person.id import DomainPersonId
from domain.person.feature import DomainPersonFeature
from domain.image import DomainImage
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainPersonSnapshot(DomainUtilsBase):
    """
    人物検出結果のドメインモデル
    """
    id: DomainId
    location: DomainLocation
    timestamp: DomainTimestamp
    image: DomainImage
    person_id: DomainPersonId
    feature: DomainPersonFeature
    answer_person_id: DomainPersonId
