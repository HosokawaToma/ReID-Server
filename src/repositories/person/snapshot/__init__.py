from repositories import RepositoryDatabase
from entities.person.snapshot import EntityPersonSnapshot
from migration.models.person_snapshots import MigrationModelPersonSnapshot
import torch
from dataclasses import dataclass
import uuid
from datetime import datetime
from environment import Environment
from sqlalchemy.orm import Query
@dataclass
class RepositoryPersonSnapshotFilters:
    ids: list[uuid.UUID] | None = None
    not_ids: list[uuid.UUID] | None = None
    image_ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    person_ids: list[uuid.UUID] | None = None
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None

@dataclass
class RepositoryPersonSnapshotOrdering:
    feature_to_nearest: torch.Tensor | None = None
    timestamp_asc: bool | None = None
    timestamp_desc: bool | None = None

class RepositoryPersonSnapshotError(Exception):
    pass

class PersonSnapshotNotFoundError(RepositoryPersonSnapshotError):
    pass

class RepositoryPersonSnapshot:
    def __init__(
        self,
        database: RepositoryDatabase,
        ):
        self.database = database

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshot":
        return cls(
            database=RepositoryDatabase(environment),
        )

    def _build_filters(self, query: Query, filters: RepositoryPersonSnapshotFilters) -> Query:
        if filters is not None and filters.ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.id.in_(filters.ids))
        if filters is not None and filters.not_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.id.not_in(filters.not_ids))
        if filters is not None and filters.image_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.image_id.in_(filters.image_ids))
        if filters is not None and filters.camera_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.camera_id.in_(filters.camera_ids))
        if filters is not None and filters.view_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.view_id.in_(filters.view_ids))
        if filters is not None and filters.person_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.person_id.in_(filters.person_ids))
        if filters is not None and filters.after_timestamp is not None:
            query = query.filter(MigrationModelPersonSnapshot.timestamp >= filters.after_timestamp)
        if filters is not None and filters.before_timestamp is not None:
            query = query.filter(MigrationModelPersonSnapshot.timestamp <= filters.before_timestamp)
        return query

    def _build_ordering(self, query: Query, ordering: RepositoryPersonSnapshotOrdering) -> Query:
        order_by = []
        if ordering is not None and ordering.feature_to_nearest is not None:
            order_by.append(MigrationModelPersonSnapshot.feature.op("<=>")(ordering.feature_to_nearest.cpu().numpy().tolist()))
        if ordering is not None and ordering.timestamp_asc is not None:
            order_by.append(MigrationModelPersonSnapshot.timestamp.asc())
        if ordering is not None and ordering.timestamp_desc is not None:
            order_by.append(MigrationModelPersonSnapshot.timestamp.desc())
        if len(order_by) > 0:
            query = query.order_by(*order_by)
        return query

    def model_to_entity(self, model: MigrationModelPersonSnapshot) -> EntityPersonSnapshot:
        return EntityPersonSnapshot(
            id=uuid.UUID(str(model.id)),
            image_id=uuid.UUID(str(model.image_id)),
            camera_id=int(str(model.camera_id)),
            view_id=int(str(model.view_id)),
            timestamp=datetime.fromisoformat(str(model.timestamp)),
            person_id=uuid.UUID(str(model.person_id)),
            feature=torch.tensor(model.feature) if model.feature is not None else None,
        )

    def save(self, snapshot: EntityPersonSnapshot) -> None:
        with self.database as session:
            session.add(MigrationModelPersonSnapshot(
                id=snapshot.id,
                image_id=snapshot.image_id,
                camera_id=snapshot.camera_id,
                view_id=snapshot.view_id,
                timestamp=snapshot.timestamp,
                person_id=snapshot.person_id,
                feature=snapshot.feature.cpu().numpy().tolist() if snapshot.feature is not None else None
            ))

    def find_first(
        self,
        filters: RepositoryPersonSnapshotFilters | None = None,
        ordering: RepositoryPersonSnapshotOrdering | None = None,
    ) -> EntityPersonSnapshot:
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot)
            if filters is not None:
                query = self._build_filters(query, filters)
            if ordering is not None:
                query = self._build_ordering(query, ordering)
            model = query.first()
            if model is None:
                raise PersonSnapshotNotFoundError
            return self.model_to_entity(model)

    def find(
        self,
        filters: RepositoryPersonSnapshotFilters | None = None,
        ordering: RepositoryPersonSnapshotOrdering | None = None,
    ) -> list[EntityPersonSnapshot]:
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot)
            if filters is not None:
                query = self._build_filters(query, filters)
            if ordering is not None:
                query = self._build_ordering(query, ordering)
            models = query.all()
            return [self.model_to_entity(model) for model in models]

    def update(
        self,
        person_snapshot: EntityPersonSnapshot,
        filters: RepositoryPersonSnapshotFilters | None = None,
    ) -> None:
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot)
            if filters is not None:
                query = self._build_filters(query, filters)
            query.update(
                {
                    MigrationModelPersonSnapshot.image_id: person_snapshot.image_id,
                    MigrationModelPersonSnapshot.camera_id: person_snapshot.camera_id,
                    MigrationModelPersonSnapshot.view_id: person_snapshot.view_id,
                    MigrationModelPersonSnapshot.timestamp: person_snapshot.timestamp,
                    MigrationModelPersonSnapshot.person_id: person_snapshot.person_id,
                    MigrationModelPersonSnapshot.feature: person_snapshot.feature.cpu().numpy().tolist() if person_snapshot.feature is not None else None,
                }
            )

    def delete(
        self,
        filters: RepositoryPersonSnapshotFilters | None = None,
    ) -> None:
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot)
            if filters is not None:
                query = self._build_filters(query, filters)
            query.delete()
