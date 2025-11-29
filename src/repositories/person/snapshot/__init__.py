from repositories import RepositoryDatabase
from entities.person.snapshot import EntityPersonSnapshot
from migration.models.person_snapshots import MigrationModelPersonSnapshot
import torch
from dataclasses import dataclass
import uuid
from datetime import datetime
from environment import Environment

@dataclass
class RepositoryPersonSnapshotFindOneFilters:
    ids: list[uuid.UUID] | None = None

@dataclass
class RepositoryPersonSnapshotFindOneOrdering:
    feature_to_nearest: torch.Tensor | None = None

@dataclass
class RepositoryPersonSnapshotFindOneParams:
    filters: RepositoryPersonSnapshotFindOneFilters | None = None
    ordering: RepositoryPersonSnapshotFindOneOrdering | None = None

@dataclass
class RepositoryPersonSnapshotFindFilters:
    ids: list[uuid.UUID] | None = None
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None

@dataclass
class RepositoryPersonSnapshotFindParams:
    filters: RepositoryPersonSnapshotFindFilters | None = None

@dataclass
class RepositoryPersonSnapshotUpdateParams:
    ids: list[uuid.UUID]

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

    def find_first(self, params: RepositoryPersonSnapshotFindOneParams) -> EntityPersonSnapshot:
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot)
            if params.filters is not None and params.filters.ids is not None:
                query = query.filter(MigrationModelPersonSnapshot.id.in_(params.filters.ids))
            if params.ordering is not None and params.ordering.feature_to_nearest is not None:
                query = query.order_by(MigrationModelPersonSnapshot.feature.op("<=>")(params.ordering.feature_to_nearest.cpu().numpy().tolist()))
            model = query.first()
            if model is None:
                raise PersonSnapshotNotFoundError
            return EntityPersonSnapshot(
                id=uuid.UUID(str(model.id)),
                image_id=uuid.UUID(str(model.image_id)),
                camera_id=int(str(model.camera_id)),
                view_id=int(str(model.view_id)),
                timestamp=datetime.fromisoformat(str(model.timestamp)),
                person_id=uuid.UUID(str(model.person_id)),
                feature=torch.tensor(model.feature) if model.feature is not None else None,
            )

    def find(self, params: RepositoryPersonSnapshotFindParams) -> list[EntityPersonSnapshot]:
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot)
            if params.filters is not None and params.filters.ids is not None:
                query = query.filter(MigrationModelPersonSnapshot.id.in_(params.filters.ids))
            if params.filters is not None and params.filters.after_timestamp is not None:
                query = query.filter(MigrationModelPersonSnapshot.timestamp >= params.filters.after_timestamp)
            if params.filters is not None and params.filters.before_timestamp is not None:
                query = query.filter(MigrationModelPersonSnapshot.timestamp <= params.filters.before_timestamp)
            if params.filters is not None and params.filters.camera_ids is not None:
                query = query.filter(MigrationModelPersonSnapshot.camera_id.in_(params.filters.camera_ids))
            if params.filters is not None and params.filters.view_ids is not None:
                query = query.filter(MigrationModelPersonSnapshot.view_id.in_(params.filters.view_ids))
            models = query.all()
            return [EntityPersonSnapshot(
                id=uuid.UUID(str(model.id)),
                image_id=uuid.UUID(str(model.image_id)),
                camera_id=int(str(model.camera_id)),
                view_id=int(str(model.view_id)),
                timestamp=datetime.fromisoformat(str(model.timestamp)),
                person_id=uuid.UUID(str(model.person_id)),
                feature=torch.tensor(model.feature) if model.feature is not None else None,
            ) for model in models]

    def update(self, person_snapshot: EntityPersonSnapshot) -> None:
        with self.database as session:
            session.query(MigrationModelPersonSnapshot).filter(MigrationModelPersonSnapshot.id == person_snapshot.id).update(
                {
                    MigrationModelPersonSnapshot.image_id: person_snapshot.image_id,
                    MigrationModelPersonSnapshot.camera_id: person_snapshot.camera_id,
                    MigrationModelPersonSnapshot.view_id: person_snapshot.view_id,
                    MigrationModelPersonSnapshot.timestamp: person_snapshot.timestamp,
                    MigrationModelPersonSnapshot.person_id: person_snapshot.person_id,
                    MigrationModelPersonSnapshot.feature: person_snapshot.feature.cpu().numpy().tolist() if person_snapshot.feature is not None else None,
                }
            )
