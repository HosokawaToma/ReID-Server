from dataclasses import dataclass
from domain.person.snapshot.detail import DomainPersonSnapshotDetail
from domain.utils.sequence_base import DomainUtilsSequenceBase
from domain.person.flow import DomainPersonFlow
from domain.person.flow.sequence import DomainPersonFlowSequence
from domain.time import DomainTime
from typing import ClassVar

@dataclass(frozen=True)
class DomainPersonSnapshotDetailSequence(DomainUtilsSequenceBase[DomainPersonSnapshotDetail]):
    INTERVAL: ClassVar[DomainTime] = DomainTime(total_seconds=10)

    def to_flows(self) -> DomainPersonFlowSequence:
        if len(self.items) < 2:
            raise ValueError("人流計算には人物検出が2回以上必要です")
        first_person_id = self.items[0].person_id
        if first_person_id.id is None:
            raise ValueError("人流計算には人物IDが必要です")
        if not all(detail.person_id == first_person_id for detail in self.items):
            raise ValueError("同じ人物IDのみの人物検出の集合が必要です")
        details = sorted(self.items, key=lambda x: x.timestamp)
        flows = []
        for i in range(len(details)):
            if i == 0:
                continue
            if details[i].location.camera_id == details[i - 1].location.camera_id \
                and details[i].timestamp - details[i - 1].timestamp <= self.INTERVAL:
                continue
            flows.append(DomainPersonFlow(
                person_id=first_person_id.id,
                source_location=details[i - 1].location,
                target_location=details[i].location,
                source_timestamp=details[i - 1].timestamp,
                target_timestamp=details[i].timestamp,
            ))
        return DomainPersonFlowSequence(items=flows)
