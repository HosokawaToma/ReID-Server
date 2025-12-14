from dataclasses import dataclass
from datetime import timedelta
from typing import ClassVar, Iterator
from domain.person.snapshot import DomainPersonSnapshot
import uuid
from domain.person.flow import DomainPersonFlow
from domain.person.flow_sequence import DomainPersonFlowSequence
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtractionQueueItem

@dataclass
class DomainPersonSnapshotSequence:
    INTERVAL: ClassVar[timedelta] = timedelta(seconds=10)
    person_snapshots: list[DomainPersonSnapshot]

    def __iter__(self) -> Iterator[DomainPersonSnapshot]:
        return iter(self.person_snapshots)

    def to_feature_extraction_queue_items(self) -> list[RepositoryQueuePersonSnapshotFeatureExtractionQueueItem]:
        return [
            RepositoryQueuePersonSnapshotFeatureExtractionQueueItem(
                id=person_snapshot.id,
            ) for person_snapshot in self.person_snapshots
        ]

    def group_by_person_id(self) -> list["DomainPersonSnapshotSequence"]:
        person_snapshots_by_person_id: dict[uuid.UUID, list[DomainPersonSnapshot]] = {}
        for person_snapshot in self.person_snapshots:
            if person_snapshot.person_id is None:
                continue
            if person_snapshot.person_id not in person_snapshots_by_person_id:
                person_snapshots_by_person_id[person_snapshot.person_id] = []
            person_snapshots_by_person_id[person_snapshot.person_id].append(person_snapshot)
        return [
            DomainPersonSnapshotSequence(person_snapshots=person_snapshots)
            for _, person_snapshots in person_snapshots_by_person_id.items()
        ]

    def person_id(self) -> uuid.UUID | None:
        if len(self.person_snapshots) == 0:
            return None
        for i in range(len(self.person_snapshots)):
            if i == 0:
                continue
            if self.person_snapshots[i].person_id != self.person_snapshots[i - 1].person_id:
                return None
        return self.person_snapshots[0].person_id

    def to_flows(self) -> DomainPersonFlowSequence | None:
        grouped_person_snapshots = self.group_by_person_id()
        flows = []
        for grouped_person_snapshot in grouped_person_snapshots:
            if len(grouped_person_snapshot.person_snapshots) < 2:
                continue
            person_id = grouped_person_snapshot.person_id()
            if person_id is None:
                continue
            person_snapshots = sorted(grouped_person_snapshot.person_snapshots, key=lambda x: x.timestamp)
            for i in range(len(person_snapshots)):
                if i == 0:
                    continue
                if person_snapshots[i].camera_id == person_snapshots[i - 1].camera_id \
                and person_snapshots[i].timestamp - person_snapshots[i - 1].timestamp < self.INTERVAL:
                    continue
                flows.append(DomainPersonFlow(
                    person_id=person_id,
                    source_camera_id=person_snapshots[i - 1].camera_id,
                    target_camera_id=person_snapshots[i].camera_id,
                    source_timestamp=person_snapshots[i - 1].timestamp,
                    target_timestamp=person_snapshots[i].timestamp,
                ))
        return DomainPersonFlowSequence(flows=flows)
