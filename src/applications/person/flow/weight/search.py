from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotFindError
from dataclasses import dataclass
import uuid
from datetime import datetime
from environment import Environment
from error import Error

@dataclass
class ApplicationPersonFlowWeightSearchParams:
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    person_ids: list[uuid.UUID] | None = None

@dataclass
class ApplicationPersonFlowWeightSearchItem:
    target_camera_id: int
    source_camera_id: int
    weight: int

class ApplicationPersonFlowWeightSearchError(Error):
    pass

class ApplicationPersonFlowWeightSearch:
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonFlowWeightSearch":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment=environment),
        )

    def search(self, params: ApplicationPersonFlowWeightSearchParams | None = None) -> list[ApplicationPersonFlowWeightSearchItem]:
        try:
            filters = None
            if params is not None:
                filters = RepositoryPersonSnapshotFilters(
                    timestamp_after=params.timestamp_after,
                    timestamp_before=params.timestamp_before,
                    person_ids=params.person_ids,
                )
            person_snapshots = self.repository_person_snapshot.find(filters=filters)
            flows = person_snapshots.to_flows()
            if flows is None:
                raise ApplicationPersonFlowWeightSearchError("No flows found")
            return [ApplicationPersonFlowWeightSearchItem(
                target_camera_id=flow_weight.target_camera_id,
                source_camera_id=flow_weight.source_camera_id,
                weight=flow_weight.weight,
            ) for flow_weight in flows.to_weights()]
        except RepositoryPersonSnapshotFindError as error:
            raise ApplicationPersonFlowWeightSearchError(error.message) from error
