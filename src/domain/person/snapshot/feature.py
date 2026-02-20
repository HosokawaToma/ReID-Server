"""
人物スナップショット特徴量のドメインモデル

検出結果の ID・位置・タイムスタンプ・特徴量・人物ID を保持し、ReID 判定を提供する。
"""
from dataclasses import dataclass
from domain.person.feature import DomainPersonFeature
from domain.utils.base import DomainUtilsBase
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.person.id import DomainPersonId


@dataclass(frozen=True)
class DomainPersonSnapshotFeature(DomainUtilsBase):
    """
    人物検出結果の特徴量のドメインモデル
    """
    id: DomainId
    location: DomainLocation
    timestamp: DomainTimestamp
    feature: DomainPersonFeature
    person_id: DomainPersonId

    def reid(self, nearest_person_snapshot_feature: "DomainPersonSnapshotFeature") -> "DomainPersonSnapshotFeature":
        """
        最も近い人物検出結果の特徴量との類似度を計算し同一人物と判定された場合は最も近い人物検出結果の人物IDを使用する
        :param DomainPersonSnapshotFeature nearest_person_snapshot_feature: 最も近い人物検出結果の特徴量
        :return DomainPersonSnapshotFeature: 最も近い人物検出結果の人物IDを使用した人物検出結果の特徴量
        """
        if self.feature.is_same(nearest_person_snapshot_feature.feature):
            return DomainPersonSnapshotFeature(
                id=self.id,
                location=self.location,
                timestamp=self.timestamp,
                feature=self.feature,
                person_id=nearest_person_snapshot_feature.person_id.copy(),
            )
        return DomainPersonSnapshotFeature(
            id=self.id,
            location=self.location,
            timestamp=self.timestamp,
            feature=self.feature,
            person_id=self.person_id.copy(),
        )
