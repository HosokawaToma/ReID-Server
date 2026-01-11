from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from environment import Environment
from error import Error
from applications import ApplicationBase
from dto.person.flow.weight.query import DtoPersonFlowWeightQuery
from dto.person.flow.weight import DtoPersonFlowWeight

class ApplicationPersonFlowWeightSearchError(Error):
    pass

class ApplicationPersonFlowWeightSearchNoFlowsFoundError(ApplicationPersonFlowWeightSearchError):
    pass

class ApplicationPersonFlowWeightSearch(ApplicationBase):
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonFlowWeightSearch":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment=environment),
        )

    def search(self, query: DtoPersonFlowWeightQuery | None = None) -> list[DtoPersonFlowWeight]:
        filters = None
        if query is not None:
            filters = RepositoryPersonSnapshotFilters(
                timestamp_after=query.timestamp_after,
                timestamp_before=query.timestamp_before,
                person_ids=query.person_ids,
            )
        try:
            person_snapshots = self.repository_person_snapshot.find(filters=filters)
            flows = person_snapshots.to_flows()
        except Error as error:
            raise ApplicationPersonFlowWeightSearchError(error) from error
        if flows is None:
            raise ApplicationPersonFlowWeightSearchNoFlowsFoundError()
        return [DtoPersonFlowWeight(
            target_camera_id=flow_weight.target_camera_id,
            source_camera_id=flow_weight.source_camera_id,
            weight=flow_weight.weight,
        ) for flow_weight in flows.to_weights()]
