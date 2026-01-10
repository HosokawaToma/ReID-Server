from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from environment import Environment
from error import Error
from applications import ApplicationBase
from dto.person.flow import DtoPersonFlow
from dto.person.flow.query import DtoPersonFlowQuery

class ApplicationPersonFlowSearchError(Error):
    pass

class ApplicationPersonFlowSearchNoFlowsFoundError(ApplicationPersonFlowSearchError):
    pass

class ApplicationPersonFlowSearch(ApplicationBase):
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

    def search(self, query: DtoPersonFlowQuery) -> list[DtoPersonFlow]:
        filters = RepositoryPersonSnapshotFilters(
            timestamp_after=query.timestamp_after,
            timestamp_before=query.timestamp_before,
            person_ids=[query.person_id],
        )
        try:
            person_snapshots = self.repository_person_snapshot.find(filters=filters)
            flows = person_snapshots.to_flows()
        except Error as error:
            raise ApplicationPersonFlowSearchError(error) from error
        if flows is None:
            raise ApplicationPersonFlowSearchNoFlowsFoundError()
        return [DtoPersonFlow(
            person_id=query.person_id,
            source_camera_id=flow.source_camera_id,
            target_camera_id=flow.target_camera_id,
            source_timestamp=flow.source_timestamp,
            target_timestamp=flow.target_timestamp,
        ) for flow in flows.flows]
