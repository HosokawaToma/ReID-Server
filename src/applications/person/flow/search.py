from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFindParams
from repositories.person.snapshot import RepositoryPersonSnapshotFindFilters
from sequences.person.flows import SequencePersonFlows
from sequences.person.snapshots import SequencePersonSnapshots
from modules.person.flow.calculator import ModulePersonFlowCalculator
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
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
        module_person_flow_calculator: ModulePersonFlowCalculator,
    ):
        self.repository_person_snapshot = repository_person_snapshot
        self.module_person_flow_calculator = module_person_flow_calculator

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonFlowSearch":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment=environment,
            ),
            module_person_flow_calculator=ModulePersonFlowCalculator(
                interval=timedelta(seconds=10),
            ),
        )

    def search(self, params: ApplicationPersonFlowSearchParams | None = None) -> list[SequencePersonFlows]:
        filters = None
        if params is not None:
            filters = RepositoryPersonSnapshotFindFilters(
                after_timestamp=params.after_timestamp,
                before_timestamp=params.before_timestamp,
                person_ids=params.person_ids,
            )
        person_snapshots = SequencePersonSnapshots(
            person_snapshots=self.repository_person_snapshot.find(
                params=RepositoryPersonSnapshotFindParams(filters=filters),
            )
        )
        return [
            self.module_person_flow_calculator.calculate(item)
            for item in person_snapshots.group_by_person_id()
            ]
