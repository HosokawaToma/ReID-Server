from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from environment import Environment
from datetime import datetime
from error import Error
import uuid
from dataclasses import dataclass
from applications import ApplicationBase

@dataclass
class ApplicationPersonFlowSearchParams:
    person_id: uuid.UUID
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

@dataclass
class ApplicationPersonFlowSearchItem:
    person_id: uuid.UUID
    source_camera_id: int
    target_camera_id: int
    source_timestamp: datetime
    target_timestamp: datetime

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

    def search(self, params: ApplicationPersonFlowSearchParams) -> list[ApplicationPersonFlowSearchItem]:
        filters = RepositoryPersonSnapshotFilters(
            timestamp_after=params.timestamp_after,
            timestamp_before=params.timestamp_before,
            person_ids=[params.person_id],
        )
        try:
            person_snapshots = self.repository_person_snapshot.find(filters=filters)
            flows = person_snapshots.to_flows()
        except Error as error:
            raise ApplicationPersonFlowSearchError(error) from error
        if flows is None:
            raise ApplicationPersonFlowSearchNoFlowsFoundError()
        return [ApplicationPersonFlowSearchItem(
            person_id=params.person_id,
            source_camera_id=flow.source_camera_id,
            target_camera_id=flow.target_camera_id,
            source_timestamp=flow.source_timestamp,
            target_timestamp=flow.target_timestamp,
        ) for flow in flows.flows]
