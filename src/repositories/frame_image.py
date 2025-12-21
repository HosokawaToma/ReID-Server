from repositories import RepositoryStorage
from repositories import RepositoryStorageImage
from repositories import RepositoryStorageImageName
from repositories import RepositoryRedis
from error import Error
from domain.frame_image import DomainFrameImage
from environment import Environment
import uuid
from PIL import Image
from typing import Literal
from datetime import datetime


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

QueueName = Literal["frame_image:person_snapshot_create"]

class RepositoryFrameImage:
    def __init__(self, storage: RepositoryStorage, redis: RepositoryRedis):
        self.storage = storage
        self.redis = redis

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryFrameImage":
        return cls(
            storage=RepositoryStorage.create(
                environment,
                directory="frame_images",
            ),
            redis=RepositoryRedis.create(
                environment,
            ),
        )

    def save(self, frame_image: DomainFrameImage) -> None:
        try:
            self.storage.image_save(RepositoryStorageImage(
                name=str(frame_image.id),
                image=frame_image.image,
            ))
        except Error as error:
            raise RepositoryFrameImageSaveError(error) from error

    def next_queue(self, queue_name: QueueName) -> DomainFrameImage:
        try:
            data = self.redis.dequeue(queue_name)
            return DomainFrameImage(
                id=uuid.UUID(data["id"]),
                image=self.storage.image_find_one(RepositoryStorageImageName(
                    name=str(data["id"]))).image,
                camera_id=int(data["camera_id"]),
                view_id=int(data["view_id"]),
                timestamp=datetime.fromisoformat(data["timestamp"]),
            )
        except Error as error:
            raise RepositoryFrameImageNextQueueError(error) from error

    def push_queue(self, queue_name: QueueName, frame_image: DomainFrameImage) -> None:
        try:
            self.redis.push(
                key=queue_name,
                value={
                    "id": str(frame_image.id),
                    "camera_id": str(frame_image.camera_id),
                    "view_id": str(frame_image.view_id),
                    "timestamp": frame_image.timestamp.isoformat(),
                }
            )
        except Error as error:
            raise RepositoryFrameImagePushQueueError(error) from error

    def find_image(self, id: uuid.UUID) -> Image.Image:
        try:
            return self.storage.image_find_one(RepositoryStorageImageName(
                name=str(id))).image
        except Error as error:
            raise RepositoryFrameImageFindImageError(error) from error

    def delete(self, frame_image: DomainFrameImage) -> None:
        try:
            self.storage.image_delete(RepositoryStorageImageName(
                name=str(frame_image.id),
            ))
        except Error as error:
            raise RepositoryFrameImageDeleteError(error) from error
