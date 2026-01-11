from repositories import RepositoryStorage
from repositories import RepositoryStorageImage
from repositories import RepositoryStorageImageName
from repositories import RepositoryRedis
from repositories import RepositoryDatabase
from migration.models.frame_images import MigrationModelFrameImage
from error import Error
from domain.frame_image import DomainFrameImage
from domain.frame_image.filter import DomainFrameImageFilter
from domain.frame_image.ordering import DomainFrameImageOrdering
from environment import Environment
from domain.frame_image.meta_data import DomainFrameImageMetaData
import uuid
from datetime import datetime
from PIL import Image
from sqlalchemy.orm import Query


class RepositoryFrameImageError(Error):
    pass
class RepositoryFrameImageSaveError(RepositoryFrameImageError):
    pass
class RepositoryFrameImageFindError(RepositoryFrameImageError):
    pass
class RepositoryFrameImageOrderingError(RepositoryFrameImageError):
    pass
class RepositoryFrameImageNextQueueError(RepositoryFrameImageError):
    pass
class RepositoryFrameImagePushQueueError(RepositoryFrameImageError):
    pass
class RepositoryFrameImageFindImageError(RepositoryFrameImageError):
    pass
class RepositoryFrameImageDeleteError(RepositoryFrameImageError):
    pass

class RepositoryFrameImage:
    def __init__(self, database: RepositoryDatabase, storage: RepositoryStorage, redis: RepositoryRedis):
        self.database = database
        self.storage = storage
        self.redis = redis

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryFrameImage":
        return cls(
            database=RepositoryDatabase.create(
                environment,
            ),
            storage=RepositoryStorage.create(
                environment,
                directory="frame_images",
            ),
            redis=RepositoryRedis.create(
                environment,
            ),
        )

    def _model_to_domain(self, model: MigrationModelFrameImage, image: Image.Image) -> DomainFrameImage:
        return DomainFrameImage(
            id=uuid.UUID(str(model.id)),
            image=image,
            camera_id=int(str(model.camera_id)),
            view_id=int(str(model.view_id)),
            timestamp=datetime.fromisoformat(str(model.timestamp)),
        )

    def _model_to_domain_meta_data(self, model: MigrationModelFrameImage) -> DomainFrameImageMetaData:
        return DomainFrameImageMetaData(
            id=uuid.UUID(str(model.id)),
            camera_id=int(str(model.camera_id)),
            view_id=int(str(model.view_id)),
            timestamp=datetime.fromisoformat(str(model.timestamp)),
        )

    def save(self, frame_image: DomainFrameImage) -> None:
        try:
            with self.database as session:
                session.add(MigrationModelFrameImage(
                    id=frame_image.id,
                    camera_id=frame_image.camera_id,
                    view_id=frame_image.view_id,
                    timestamp=frame_image.timestamp,
                ))
                self.storage.image_save(RepositoryStorageImage(
                    name=str(frame_image.id),
                    image=frame_image.image,
                ))
        except Error as error:
            raise RepositoryFrameImageSaveError(error) from error

    def _build_filters(self, query: Query, filters: DomainFrameImageFilter) -> Query:
        if filters.ids is not None:
            query = query.filter(
                MigrationModelFrameImage.id.in_(filters.ids))
        if filters.camera_ids is not None:
            query = query.filter(
                MigrationModelFrameImage.camera_id.in_(filters.camera_ids))
        if filters.view_ids is not None:
            query = query.filter(
                MigrationModelFrameImage.view_id.in_(filters.view_ids))
        if filters.timestamp_after is not None:
            query = query.filter(
                MigrationModelFrameImage.timestamp >= filters.timestamp_after)
        if filters.timestamp_before is not None:
            query = query.filter(
                MigrationModelFrameImage.timestamp <= filters.timestamp_before)
        return query

    def _build_ordering(self, query: Query, ordering: DomainFrameImageOrdering) -> Query:
        for order in ordering.ordering:
            if order == DomainFrameImageOrdering.KEY_TIMESTAMP_ASC:
                query = query.order_by(MigrationModelFrameImage.timestamp.asc())
            elif order == DomainFrameImageOrdering.KEY_TIMESTAMP_DESC:
                query = query.order_by(MigrationModelFrameImage.timestamp.desc())
            else:
                raise RepositoryFrameImageOrderingError()
        return query

    def find_first(self, filters: DomainFrameImageFilter | None = None, ordering: DomainFrameImageOrdering | None = None) -> DomainFrameImage:
        try:
            with self.database as session:
                query = session.query(MigrationModelFrameImage)
                if filters is not None:
                    query = self._build_filters(query, filters)
                if ordering is not None:
                    query = self._build_ordering(query, ordering)
                models = query.all()
                if len(models) == 0:
                    raise RepositoryFrameImageFindError()
                image = self.storage.image_find_one(RepositoryStorageImageName(
                    name=str(models[0].id),
                )).image
                return self._model_to_domain(models[0], image)
        except Error as error:
            raise RepositoryFrameImageFindError(error) from error

    def meta_data_find_all(self, filters: DomainFrameImageFilter | None = None, ordering: DomainFrameImageOrdering | None = None) -> list[DomainFrameImageMetaData]:
        try:
            with self.database as session:
                query = session.query(MigrationModelFrameImage)
                if filters is not None:
                    query = self._build_filters(query, filters)
                if ordering is not None:
                    query = self._build_ordering(query, ordering)
                models = query.all()
                return [self._model_to_domain_meta_data(model) for model in models]
        except Error as error:
            raise RepositoryFrameImageFindError(error) from error

    def delete(self, frame_image: DomainFrameImage) -> None:
        try:
            with self.database as session:
                query = session.query(MigrationModelFrameImage)
                query = query.filter(
                    MigrationModelFrameImage.id == frame_image.id)
                model = query.first()
                if model is None:
                    raise RepositoryFrameImageDeleteError()
                session.delete(model)
                self.storage.image_delete(RepositoryStorageImageName(
                    name=str(model.id),
                ))
        except Error as error:
            raise RepositoryFrameImageDeleteError(error) from error

    def next_person_snapshot_create(self) -> DomainFrameImage:
        try:
            data = self.redis.dequeue("frame_image:person_snapshot_create")
            with self.database as session:
                query = session.query(MigrationModelFrameImage)
                query = query.filter(
                    MigrationModelFrameImage.id == uuid.UUID(data["id"]))
                model = query.first()
                if model is None:
                    raise RepositoryFrameImageNextQueueError()
                image = self.storage.image_find_one(RepositoryStorageImageName(
                    name=str(model.id),
                )).image
                return self._model_to_domain(model, image)
        except Error as error:
            raise RepositoryFrameImageNextQueueError(error) from error

    def push_person_snapshot_create(self, frame_image: DomainFrameImage) -> None:
        try:
            self.redis.push(
                key="frame_image:person_snapshot_create",
                value={
                    "id": str(frame_image.id)
                }
            )
        except Error as error:
            raise RepositoryFrameImagePushQueueError(error) from error
