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
