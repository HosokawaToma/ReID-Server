from repositories import RepositoryStorage
from repositories import RepositoryStorageImage
from repositories import RepositoryStorageImageName
from repositories import RepositoryRedis
from repositories import RepositoryDatabase
from migration.models.frame_images import MigrationModelFrameImage
from error import Error
from domain.frame_image import DomainFrameImage
from environment import Environment
import uuid
from datetime import datetime
from PIL import Image


class RepositoryFrameImageError(Error):
    pass
class RepositoryFrameImageSaveError(RepositoryFrameImageError):
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
