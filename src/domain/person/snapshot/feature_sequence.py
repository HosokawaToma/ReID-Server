"""
人物スナップショット特徴量シーケンスのドメインモデル

特徴量のリストを保持する。
"""
from dataclasses import dataclass
from domain.person.snapshot.feature import DomainPersonSnapshotFeature
from domain.utils.sequence_base import DomainUtilsSequenceBase


@dataclass(frozen=True)
class DomainPersonSnapshotFeatureSequence(DomainUtilsSequenceBase[DomainPersonSnapshotFeature]):
    """
    人物検出結果の特徴量のシーケンスのドメインモデル
    """
    pass
