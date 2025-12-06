from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFindParams
from repositories.person.snapshot import RepositoryPersonSnapshotFindFilters
from sequences.person.snapshots import SequencePersonSnapshots
from sequences.person.flows import SequencePersonFlows
from sequences.person.flow_weights import SequencePersonFlowWeights
from dataclasses import dataclass
import uuid
from datetime import datetime, timedelta
from environment import Environment

@dataclass
class ApplicationPersonFlowWeightSearchParams:
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None
    person_ids: list[uuid.UUID] | None = None

class ApplicationPersonFlowWeightSearch:
    INTERVAL = timedelta(seconds=10)

    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonFlowWeightSearch":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment=environment),
        )


    def search(self, params: ApplicationPersonFlowWeightSearchParams | None = None) -> SequencePersonFlowWeights:
        filters = None
        if params is not None:
            filters = RepositoryPersonSnapshotFindFilters(
                after_timestamp=params.after_timestamp,
                before_timestamp=params.before_timestamp,
                person_ids=params.person_ids,
            )
        person_snapshots = SequencePersonSnapshots(
            person_snapshots=self.repository_person_snapshot.find(params=RepositoryPersonSnapshotFindParams(filters=filters)),
        )
        sequences = [
            person_snapshots.convert_to_flows(interval=self.INTERVAL)
            for person_snapshots in person_snapshots.group_by_person_id() if person_snapshots.is_convertible_to_flows()
        ]
        return SequencePersonFlows.combine(sequences=sequences).convert_to_weights()
