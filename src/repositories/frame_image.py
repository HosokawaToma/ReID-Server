from repositories import RepositoryStorage
from repositories import RepositoryStorageImage
from repositories import RepositoryStorageImageFindParams
from repositories import RepositoryStorageImageDeleteParams
from error import Error
from domain.frame_image import DomainFrameImage
from environment import Environment
import uuid
from PIL import Image
from typing import Literal
from repositories import RepositoryRedis
from datetime import datetime
from repositories import RepositoryRedisError


class RepositoryFrameImageError(Error):
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

    def next_queue(self, queue_name: QueueName) -> DomainFrameImage:
        data = self.redis.dequeue(queue_name)
        result = DomainFrameImage(
            id=uuid.UUID(data["id"]),
            image=self.storage.image_find_one(RepositoryStorageImageFindParams(
                name=str(data["id"]))).image,
            camera_id=int(data["camera_id"]),
            view_id=int(data["view_id"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )
        self.storage.image_delete(RepositoryStorageImageDeleteParams(
            name=str(data["id"]),
        ))
        return result

    def push_queue(self, queue_name: QueueName, frame_image: DomainFrameImage) -> None:
        try:
            self.storage.image_save(RepositoryStorageImage(
                name=str(frame_image.id),
                image=frame_image.image,
            ))
            self.redis.push(
                key=queue_name,
                value={
                    "id": str(frame_image.id),
                    "camera_id": str(frame_image.camera_id),
                    "view_id": str(frame_image.view_id),
                    "timestamp": frame_image.timestamp.isoformat(),
                }
            )
        except RepositoryRedisError as e:
            self.storage.image_delete(RepositoryStorageImageDeleteParams(
                name=str(frame_image.id),
            ))
            raise RepositoryFrameImageError(e.message)
