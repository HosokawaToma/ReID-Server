from repositories import RepositoryDatabase
from repositories import RepositoryStorage
from repositories import RepositoryStorageImage
from repositories import RepositoryStorageImageName
from repositories import RepositoryRedis
from domain.person.snapshot import DomainPersonSnapshot
from migration.models.person_snapshots import MigrationModelPersonSnapshot
import torch
from dataclasses import dataclass
import uuid
from environment import Environment
from sqlalchemy.orm import Query
from typing import Literal, ClassVar
from error import Error
from datetime import datetime
from domain.person.snapshot_sequence import DomainPersonSnapshotSequence
from PIL import Image
import sqlalchemy as sa


@dataclass
class RepositoryPersonSnapshotFilters:
    ids: list[uuid.UUID] | None = None
    not_ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    is_junk: bool | None = None
    person_ids: list[uuid.UUID] | None = None
    has_person_id: bool | None = None
    has_feature: bool | None = None

@dataclass
class RepositoryPersonSnapshotOrdering:
    KEY_TIMESTAMP_ASC: ClassVar[Literal["timestamp_asc"]] = "timestamp_asc"
    KEY_TIMESTAMP_DESC: ClassVar[Literal["timestamp_desc"]] = "timestamp_desc"
    ordering: list[Literal["timestamp_asc", "timestamp_desc"] | torch.Tensor]


TaskName = Literal["person_snapshot:feature_extraction",
                   "person_snapshot:identify"]


class RepositoryPersonSnapshotError(Error):
    pass


class RepositoryPersonSnapshotFindError(RepositoryPersonSnapshotError):
    pass


class RepositoryPersonSnapshotFindNotFoundError(RepositoryPersonSnapshotFindError):
    pass


class RepositoryPersonSnapshotSaveError(RepositoryPersonSnapshotError):
    pass


class RepositoryPersonSnapshotUpdateError(RepositoryPersonSnapshotError):
    pass


class RepositoryPersonSnapshotDeleteError(RepositoryPersonSnapshotError):
    pass


class RepositoryPersonSnapshotNextQueueError(RepositoryPersonSnapshotError):
    pass


class RepositoryPersonSnapshotPushQueueError(RepositoryPersonSnapshotError):
    pass


class RepositoryPersonSnapshotFindImageError(RepositoryPersonSnapshotError):
    pass


class RepositoryPersonSnapshot:
    def __init__(
        self,
        database: RepositoryDatabase,
        storage: RepositoryStorage,
        redis: RepositoryRedis,
    ):
        self.database = database
        self.storage = storage
        self.redis = redis

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshot":
        return cls(
            database=RepositoryDatabase.create(environment),
            storage=RepositoryStorage.create(
                environment, directory="person_snapshots"),
            redis=RepositoryRedis.create(environment),
        )

    def _build_filters(self, query: Query, filters: RepositoryPersonSnapshotFilters) -> Query:
        if filters.ids is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.id.in_(filters.ids))
        if filters.not_ids is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.id.notin_(filters.not_ids))
        if filters.camera_ids is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.camera_id.in_(filters.camera_ids))
        if filters.view_ids is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.view_id.in_(filters.view_ids))
        if filters.timestamp_after is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.timestamp >= filters.timestamp_after)
        if filters.timestamp_before is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.timestamp <= filters.timestamp_before)
        if filters.is_junk is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.is_junk == filters.is_junk)
        if filters.person_ids is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.person_id.in_(filters.person_ids))
        if filters.has_person_id is not None:
            if filters.has_person_id:
                query = query.filter(
                    MigrationModelPersonSnapshot.person_id.isnot(sa.null()))
            else:
                query = query.filter(
                    MigrationModelPersonSnapshot.person_id.is_(sa.null()))
        if filters.has_feature is not None:
            if filters.has_feature:
                query = query.filter(
                    MigrationModelPersonSnapshot.feature.isnot(sa.null()))
            else:
                query = query.filter(
                    MigrationModelPersonSnapshot.feature.is_(sa.null()))
        return query

    def _build_ordering(self, query: Query, ordering: RepositoryPersonSnapshotOrdering) -> Query:
        order_by = []
        for order in ordering.ordering:
            if isinstance(order, torch.Tensor):
                order_by.append(MigrationModelPersonSnapshot.feature.op(
                    "<=>")(order.cpu().numpy().tolist()))
            elif order == RepositoryPersonSnapshotOrdering.KEY_TIMESTAMP_ASC:
                order_by.append(MigrationModelPersonSnapshot.timestamp.asc())
            elif order == RepositoryPersonSnapshotOrdering.KEY_TIMESTAMP_DESC:
                order_by.append(MigrationModelPersonSnapshot.timestamp.desc())
        if len(order_by) > 0:
            query = query.order_by(*order_by)
        return query

    def _model_to_domain(self, model: MigrationModelPersonSnapshot, image: Image.Image) -> DomainPersonSnapshot:
        return DomainPersonSnapshot(
            id=uuid.UUID(str(model.id)),
            camera_id=int(str(model.camera_id)),
            view_id=int(str(model.view_id)),
            timestamp=datetime.fromisoformat(str(model.timestamp)),
            _is_junk=bool(model.is_junk),
            person_id=uuid.UUID(str(model.person_id)) if model.person_id is not None else None,
            feature=torch.tensor(
                model.feature) if model.feature is not None else None,
            image=image,
        )

    def save(self, snapshot: DomainPersonSnapshot) -> None:
        try:
            with self.database as session:
                session.add(MigrationModelPersonSnapshot(
                    id=snapshot.id,
                    camera_id=snapshot.camera_id,
                    view_id=snapshot.view_id,
                    timestamp=snapshot.timestamp,
                    is_junk=snapshot.is_junk,
                    person_id=snapshot.person_id,
                    feature=snapshot.feature.cpu().numpy().tolist(
                    ) if snapshot.feature is not None else None
                ))
                self.storage.image_save(RepositoryStorageImage(
                    name=str(snapshot.id),
                    image=snapshot.image,
                ))
        except Error as error:
            raise RepositoryPersonSnapshotSaveError(error) from error

    def find_first(
        self,
        filters: RepositoryPersonSnapshotFilters | None = None,
        ordering: RepositoryPersonSnapshotOrdering | None = None,
    ) -> DomainPersonSnapshot | None:
        try:
            with self.database as session:
                query = session.query(MigrationModelPersonSnapshot)
                if filters is not None:
                    query = self._build_filters(query, filters)
                if ordering is not None:
                    query = self._build_ordering(query, ordering)
                model = query.first()
                if model is None:
                    return None
                image = self.storage.image_find_one(RepositoryStorageImageName(
                    name=str(model.id),
                )).image
                return self._model_to_domain(model, image)
        except Error as error:
            raise RepositoryPersonSnapshotFindError(error) from error

    def find(
        self,
        filters: RepositoryPersonSnapshotFilters | None = None,
        ordering: RepositoryPersonSnapshotOrdering | None = None,
    ) -> DomainPersonSnapshotSequence:
        try:
            with self.database as session:
                query = session.query(MigrationModelPersonSnapshot)
                if filters is not None:
                    query = self._build_filters(query, filters)
                if ordering is not None:
                    query = self._build_ordering(query, ordering)
                models = query.all()
                images = self.storage.image_find_all(
                    [RepositoryStorageImageName(
                        name=str(model.id),
                    ) for model in models]
                )
                if len(models) != len(images):
                    raise RepositoryPersonSnapshotFindNotFoundError()
                return DomainPersonSnapshotSequence(
                    person_snapshots=[self._model_to_domain(
                        model, image.image) for model, image in zip(models, images)],
                )
        except Error as error:
            raise RepositoryPersonSnapshotFindError(error) from error

    def update(
        self,
        person_snapshot: DomainPersonSnapshot,
    ) -> None:
        try:
            with self.database as session:
                query = session.query(MigrationModelPersonSnapshot)
                query = query.filter(
                    MigrationModelPersonSnapshot.id == person_snapshot.id)
                query.update(
                    {
                        MigrationModelPersonSnapshot.camera_id: person_snapshot.camera_id,
                        MigrationModelPersonSnapshot.view_id: person_snapshot.view_id,
                        MigrationModelPersonSnapshot.timestamp: person_snapshot.timestamp,
                        MigrationModelPersonSnapshot.is_junk: person_snapshot._is_junk,
                        MigrationModelPersonSnapshot.person_id: person_snapshot.person_id,
                        MigrationModelPersonSnapshot.feature: person_snapshot.feature.cpu().numpy().tolist() if person_snapshot.feature is not None else None,
                    }
                )
        except Error as error:
            raise RepositoryPersonSnapshotUpdateError(error) from error

    def delete(
        self,
        filters: RepositoryPersonSnapshotFilters,
    ) -> None:
        try:
            with self.database as session:
                query = session.query(MigrationModelPersonSnapshot)
                query = self._build_filters(query, filters)
                models = query.all()
                for model in models:
                    session.delete(model)
                self.storage.image_delete_all(
                    [RepositoryStorageImageName(name=str(model.id)) for model in models])
        except Error as error:
            raise RepositoryPersonSnapshotDeleteError(error) from error

    def next_junk_detection(self) -> DomainPersonSnapshot:
        try:
            data = self.redis.dequeue("person_snapshot:junk_detection")
            with self.database as session:
                query = session.query(MigrationModelPersonSnapshot)
                query = query.filter(
                    MigrationModelPersonSnapshot.id == uuid.UUID(data["id"]))
                model = query.first()
                if model is None:
                    raise RepositoryPersonSnapshotNextQueueError()
                image = self.storage.image_find_one(RepositoryStorageImageName(
                    name=str(model.id),
                )).image
                return self._model_to_domain(model, image)
        except Error as error:
            raise RepositoryPersonSnapshotNextQueueError(error) from error

    def push_junk_detection(self, person_snapshot: DomainPersonSnapshot) -> None:
        try:
            self.redis.push(
                key="person_snapshot:junk_detection",
                value={
                    "id": str(person_snapshot.id),
                }
            )
        except Error as error:
            raise RepositoryPersonSnapshotPushQueueError(error) from error

    def next_feature_extraction(self) -> DomainPersonSnapshot:
        try:
            data = self.redis.dequeue("person_snapshot:feature_extraction")
            with self.database as session:
                query = session.query(MigrationModelPersonSnapshot)
                query = query.filter(
                    MigrationModelPersonSnapshot.id == uuid.UUID(data["id"]))
                model = query.first()
                if model is None:
                    raise RepositoryPersonSnapshotNextQueueError()
                image = self.storage.image_find_one(RepositoryStorageImageName(
                    name=str(model.id),
                )).image
                return self._model_to_domain(model, image)
        except Error as error:
            raise RepositoryPersonSnapshotNextQueueError(error) from error

    def push_feature_extraction(self, person_snapshot: DomainPersonSnapshot) -> None:
        try:
            self.redis.push(
                key="person_snapshot:feature_extraction",
                value={
                    "id": str(person_snapshot.id),
                }
            )
        except Error as error:
            raise RepositoryPersonSnapshotPushQueueError(error) from error

    def next_identify(self) -> DomainPersonSnapshot:
        try:
            data = self.redis.dequeue("person_snapshot:identify")
            with self.database as session:
                query = session.query(MigrationModelPersonSnapshot)
                query = query.filter(
                    MigrationModelPersonSnapshot.id == uuid.UUID(data["id"]))
                model = query.first()
                if model is None:
                    raise RepositoryPersonSnapshotNextQueueError()
                image = self.storage.image_find_one(RepositoryStorageImageName(
                    name=str(model.id),
                )).image
                return self._model_to_domain(model, image)
        except Error as error:
            raise RepositoryPersonSnapshotNextQueueError(error) from error

    def push_identify(self, person_snapshot: DomainPersonSnapshot) -> None:
        try:
            self.redis.push(
                key="person_snapshot:identify",
                value={
                    "id": str(person_snapshot.id),
                }
            )
        except Error as error:
            raise RepositoryPersonSnapshotPushQueueError(error) from error
