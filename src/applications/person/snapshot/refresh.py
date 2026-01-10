from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotOrdering
from environment import Environment
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from error import Error
from applications import ApplicationBase

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

    def refresh(self, query: DtoPersonSnapshotQuery | None = None) -> None:
        try:
            filters = None
            if query is not None:
                filters = RepositoryPersonSnapshotFilters(
                    timestamp_after=query.timestamp_after,
                    timestamp_before=query.timestamp_before,
                    camera_ids=query.camera_ids,
                    view_ids=query.view_ids,
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
