from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from sequences.person.flows import SequencePersonFlows
from sequences.person.snapshots import SequencePersonSnapshots
from environment import Environment
from datetime import datetime, timedelta
import uuid
from dataclasses import dataclass

@dataclass
class ApplicationPersonFlowSearchParams:
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None
    person_ids: list[uuid.UUID] | None = None

class ApplicationPersonFlowSearch:
    INTERVAL = timedelta(seconds=10)

    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonFlowSearch":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment=environment,
            ),
        )

    def search(self, params: ApplicationPersonFlowSearchParams | None = None) -> list[SequencePersonFlows]:
        filters = None
        if params is not None:
            filters = RepositoryPersonSnapshotFilters(
                after_timestamp=params.after_timestamp,
                before_timestamp=params.before_timestamp,
                person_ids=params.person_ids,
            )
        person_snapshots = SequencePersonSnapshots(
            person_snapshots=self.repository_person_snapshot.find(
                filters=filters,
            )
        )
        return [
            person_snapshots.convert_to_flows(interval=self.INTERVAL)
            for person_snapshots in person_snapshots.group_by_person_id() if person_snapshots.is_convertible_to_flows()
        ]
