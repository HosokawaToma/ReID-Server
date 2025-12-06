from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotOrdering
from entities.person.snapshot import EntityPersonSnapshot
from environment import Environment
from dataclasses import dataclass
import uuid
from datetime import datetime

@dataclass
class ApplicationPersonSnapshotSearchFilters:
    ids: list[uuid.UUID] | None = None
    image_ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    person_ids: list[uuid.UUID] | None = None
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None

@dataclass
class ApplicationPersonSnapshotSearchOrdering:
    timestamp_asc: bool | None = None
    timestamp_desc: bool | None = None

@dataclass
class ApplicationPersonSnapshotSearchParams:
    filters: ApplicationPersonSnapshotSearchFilters | None = None
    ordering: ApplicationPersonSnapshotSearchOrdering | None = None

class ApplicationPersonSnapshotSearch:
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
        params: ApplicationPersonSnapshotSearchParams,
    ) -> list[EntityPersonSnapshot]:
        filters = None
        if params.filters:
            filters = RepositoryPersonSnapshotFilters(
                ids=params.filters.ids,
                image_ids=params.filters.image_ids,
                camera_ids=params.filters.camera_ids,
                view_ids=params.filters.view_ids,
                person_ids=params.filters.person_ids,
                after_timestamp=params.filters.after_timestamp,
                before_timestamp=params.filters.before_timestamp,
            )
        ordering = None
        if params.ordering:
            ordering = RepositoryPersonSnapshotOrdering(
                timestamp_asc=params.ordering.timestamp_asc,
                timestamp_desc=params.ordering.timestamp_desc,
            )
        return self.person_snapshot_repository.find(
            filters=filters,
            ordering=ordering,
        )
