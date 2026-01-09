from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotOrdering
from environment import Environment
from dataclasses import dataclass
import uuid
from datetime import datetime
from error import Error
from applications import ApplicationBase


class ApplicationPersonSnapshotSearchError(Error):
    pass


@dataclass
class ApplicationPersonSnapshotSearchFilters:
    ids: list[uuid.UUID] | None = None
    not_ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    person_ids: list[uuid.UUID] | None = None
    is_junk: bool | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None


@dataclass
class ApplicationPersonSnapshotSearchOrdering:
    timestamp_asc: bool | None = None
    timestamp_desc: bool | None = None


@dataclass
class ApplicationPersonSnapshotSearchItem:
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    is_junk: bool
    person_id: uuid.UUID | None


class ApplicationPersonSnapshotSearch(ApplicationBase):
    def __init__(
        self,
        person_snapshot_repository: RepositoryPersonSnapshot,
    ):
        self.person_snapshot_repository = person_snapshot_repository

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotSearch":
        return cls(
            person_snapshot_repository=RepositoryPersonSnapshot.create(
                environment=environment,
            ),
        )

    def search(
        self,
        filters: ApplicationPersonSnapshotSearchFilters | None = None,
        ordering: ApplicationPersonSnapshotSearchOrdering | None = None,
    ) -> list[ApplicationPersonSnapshotSearchItem]:
        try:
            repository_filters = None
            repository_ordering = None
            if filters is not None:
                repository_filters = RepositoryPersonSnapshotFilters(
                    ids=filters.ids,
                    not_ids=filters.not_ids,
                    camera_ids=filters.camera_ids,
                    view_ids=filters.view_ids,
                    is_junk=filters.is_junk,
                    person_ids=filters.person_ids,
                    timestamp_after=filters.timestamp_after,
                    timestamp_before=filters.timestamp_before,
                )
            if ordering is not None:
                ordering_list = []
                if ordering.timestamp_asc:
                    ordering_list.append(
                        RepositoryPersonSnapshotOrdering.KEY_TIMESTAMP_ASC)
                if ordering.timestamp_desc:
                    ordering_list.append(
                        RepositoryPersonSnapshotOrdering.KEY_TIMESTAMP_DESC)
                repository_ordering = RepositoryPersonSnapshotOrdering(
                    ordering=ordering_list,
                )
            person_snapshots = self.person_snapshot_repository.find(
                filters=repository_filters, ordering=repository_ordering)
            return [ApplicationPersonSnapshotSearchItem(
                id=person_snapshot.id,
                camera_id=person_snapshot.camera_id,
                view_id=person_snapshot.view_id,
                timestamp=person_snapshot.timestamp,
                is_junk=person_snapshot.is_junk,
                person_id=person_snapshot.person_id,
            ) for person_snapshot in person_snapshots]
        except Error as error:
            raise ApplicationPersonSnapshotSearchError(error) from error
