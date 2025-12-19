from repositories import RepositoryDatabase
from repositories import RepositoryDatabaseError
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
from repositories import RepositoryStorage
from repositories import RepositoryStorageImage
from repositories import RepositoryStorageImageFindParams
from repositories import RepositoryStorageImageDeleteParams
from repositories import RepositoryStorageImageFindError
from repositories import RepositoryStorageImageDeleteError
from repositories import RepositoryRedisDequeueError
from domain.person.snapshot_sequence import DomainPersonSnapshotSequence
from repositories import RepositoryRedis
from repositories import RepositoryRedisError
from PIL import Image
from repositories import RepositoryStorageImageSaveError

@dataclass
class RepositoryPersonSnapshotFilters:
    ids: list[uuid.UUID] | None = None
    not_ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    person_ids: list[uuid.UUID] | None = None

    def __str__(self) -> str:
        string_list = []
        if self.ids is not None:
            string_list.append(f"ids: {self.ids}")
        if self.not_ids is not None:
            string_list.append(f"not_ids: {self.not_ids}")
        if self.camera_ids is not None:
            string_list.append(f"camera_ids: {self.camera_ids}")
        if self.view_ids is not None:
            string_list.append(f"view_ids: {self.view_ids}")
        if self.timestamp_after is not None:
            string_list.append(f"timestamp_after: {self.timestamp_after}")
        if self.timestamp_before is not None:
            string_list.append(f"timestamp_before: {self.timestamp_before}")
        if self.person_ids is not None:
            string_list.append(f"person_ids: {self.person_ids}")
        return ", ".join(string_list)

@dataclass
class RepositoryPersonSnapshotOrdering:
    KEY_TIMESTAMP_ASC: ClassVar[Literal["timestamp_asc"]] = "timestamp_asc"
    KEY_TIMESTAMP_DESC: ClassVar[Literal["timestamp_desc"]] = "timestamp_desc"
    ordering: list[Literal["timestamp_asc", "timestamp_desc"] | torch.Tensor]

TaskName = Literal["person_snapshot:feature_extraction", "person_snapshot:identify"]

class RepositoryPersonSnapshotError(Error):
    pass
class RepositoryPersonSnapshotFindError(RepositoryPersonSnapshotError):
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
            storage=RepositoryStorage.create(environment, directory="person_snapshots"),
            redis=RepositoryRedis.create(environment),
        )

    def _build_filters(self, query: Query, filters: RepositoryPersonSnapshotFilters) -> Query:
        if filters.ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.id.in_(filters.ids))
        if filters.not_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.id.notin_(filters.not_ids))
        if filters.camera_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.camera_id.in_(filters.camera_ids))
        if filters.view_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.view_id.in_(filters.view_ids))
        if filters.timestamp_after is not None:
            query = query.filter(MigrationModelPersonSnapshot.timestamp >= filters.timestamp_after)
        if filters.timestamp_before is not None:
            query = query.filter(MigrationModelPersonSnapshot.timestamp <= filters.timestamp_before)
        if filters.person_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.person_id.in_(filters.person_ids))
        return query

    def _build_ordering(self, query: Query, ordering: RepositoryPersonSnapshotOrdering) -> Query:
        order_by = []
        for order in ordering.ordering:
            if isinstance(order, torch.Tensor):
                order_by.append(MigrationModelPersonSnapshot.feature.op("<=>")(order.cpu().numpy().tolist()))
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
            person_id=uuid.UUID(str(model.person_id)),
            feature=torch.tensor(model.feature) if model.feature is not None else None,
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
                    person_id=snapshot.person_id,
                    feature=snapshot.feature.cpu().numpy().tolist() if snapshot.feature is not None else None
                ))
            self.storage.image_save(RepositoryStorageImage(
                name=str(snapshot.id),
                image=snapshot.image,
            ))
        except RepositoryDatabaseError as error:
            raise RepositoryPersonSnapshotSaveError(error.message) from error
        except RepositoryStorageImageSaveError as error:
            raise RepositoryPersonSnapshotSaveError(error.message) from error

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
                image = self.storage.image_find_one(RepositoryStorageImageFindParams(
                    name=str(model.id),
                )).image
                return self._model_to_domain(model, image)
        except RepositoryStorageImageFindError as error:
            raise RepositoryPersonSnapshotFindError(error.message) from error
        except RepositoryDatabaseError as error:
            raise RepositoryPersonSnapshotFindError(error.message) from error

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
                #Todo: N + 1問題が発生しているため修正対象
                images = [self.storage.image_find_one(RepositoryStorageImageFindParams(
                    name=str(model.id),
                )).image for model in models]
                return DomainPersonSnapshotSequence(
                    person_snapshots=[self._model_to_domain(model, image) for model, image in zip(models, images)],
                )
        except RepositoryStorageImageFindError as error:
            raise RepositoryPersonSnapshotFindError(error.message) from error
        except RepositoryDatabaseError as error:
            raise RepositoryPersonSnapshotFindError(error.message) from error

    def update(
        self,
        person_snapshot: DomainPersonSnapshot,
    ) -> None:
        try:
            with self.database as session:
                query = session.query(MigrationModelPersonSnapshot)
                query = query.filter(MigrationModelPersonSnapshot.id == person_snapshot.id)
                query.update(
                    {
                        MigrationModelPersonSnapshot.camera_id: person_snapshot.camera_id,
                        MigrationModelPersonSnapshot.view_id: person_snapshot.view_id,
                        MigrationModelPersonSnapshot.timestamp: person_snapshot.timestamp,
                        MigrationModelPersonSnapshot.person_id: person_snapshot.person_id,
                        MigrationModelPersonSnapshot.feature: person_snapshot.feature.cpu().numpy().tolist() if person_snapshot.feature is not None else None,
                    }
                )
        except RepositoryDatabaseError as error:
            raise RepositoryPersonSnapshotUpdateError(error.message) from error

    def delete(
        self,
        filters: RepositoryPersonSnapshotFilters,
    ) -> int:
        try:
            with self.database as session:
                query = session.query(MigrationModelPersonSnapshot)
                query = self._build_filters(query, filters)
                result = query.delete(synchronize_session=False)
                self.storage.image_delete(RepositoryStorageImageDeleteParams(
                        name=str(filters.ids),
                    ))
                return result
        except RepositoryDatabaseError as error:
            raise RepositoryPersonSnapshotDeleteError(error.message) from error
        except RepositoryStorageImageDeleteError as error:
            raise RepositoryPersonSnapshotDeleteError(error.message) from error

    def next_queue(self, task_name: TaskName) -> DomainPersonSnapshot:
        try:
            data = self.redis.dequeue(task_name)
            with self.database as session:
                query = session.query(MigrationModelPersonSnapshot)
                query = query.filter(MigrationModelPersonSnapshot.id == uuid.UUID(data["id"]))
                model = query.first()
                if model is None:
                    raise RepositoryPersonSnapshotNextQueueError(f"person snapshot not found: {data['id']}")
                image = self.storage.image_find_one(RepositoryStorageImageFindParams(
                    name=str(model.id),
                )).image
                return self._model_to_domain(model, image)
        except RepositoryDatabaseError as error:
            raise RepositoryPersonSnapshotNextQueueError(error.message) from error
        except RepositoryRedisDequeueError as error:
            raise RepositoryPersonSnapshotNextQueueError(error.message) from error
        except RepositoryStorageImageFindError as error:
            raise RepositoryPersonSnapshotNextQueueError(error.message) from error

    def push_queue(self, task_name: TaskName, person_snapshot: DomainPersonSnapshot) -> None:
        try:
            self.redis.push(
                key=task_name,
                value={
                    "id": str(person_snapshot.id),
                }
            )
        except RepositoryRedisError as error:
            raise RepositoryPersonSnapshotPushQueueError(error.message) from error
