from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotOrdering
from environment import Environment
from datetime import datetime
from dataclasses import dataclass
from error import Error
from applications import ApplicationBase

@dataclass
class ApplicationPersonSnapshotRefreshParams:
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None

class ApplicationPersonSnapshotRefreshError(Error):
    pass

class ApplicationPersonSnapshotRefresh(ApplicationBase):
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotRefresh":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
        )

    def refresh(self, params: ApplicationPersonSnapshotRefreshParams | None = None) -> None:
        try:
            filters = None
            if params is not None:
                filters = RepositoryPersonSnapshotFilters(
                    timestamp_after=params.timestamp_after,
                    timestamp_before=params.timestamp_before,
                    camera_ids=params.camera_ids,
                    view_ids=params.view_ids,
                )
            person_snapshots = self.repository_person_snapshot.find(
                filters=filters,
                ordering=RepositoryPersonSnapshotOrdering(
                    ordering=[RepositoryPersonSnapshotOrdering.KEY_TIMESTAMP_ASC],
                ),
            )
            for person_snapshot in person_snapshots:
                self.repository_person_snapshot.push_junk_detection(person_snapshot)
        except Error as error:
            raise ApplicationPersonSnapshotRefreshError(error) from error
