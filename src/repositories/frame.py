from repositories import RepositoryStorage
from repositories import RepositoryStorageImage
from repositories import RepositoryStorageImageFindOneParams
from repositories import RepositoryStorageImageDeleteParams
from repositories import RepositoryStorageImageError
from error import Error
from entities.frame import EntityFrame
from environment import Environment
from dataclasses import dataclass
import uuid
from datetime import datetime

@dataclass
class RepositoryFrameFindParams:
    id: uuid.UUID | None = None
    camera_id: int | None = None
    view_id: int | None = None
    timestamp: datetime | None = None

@dataclass
class RepositoryFrameDeleteParams:
    id: uuid.UUID

class RepositoryFrameError(Error):
    pass

class RepositoryFrame:
    IMAGE_NAME_TEMPLATE = "{id}_{camera_id}_{view_id}_{timestamp}"
    SPLIT_PATTERN = "_"

    def __init__(self, storage: RepositoryStorage):
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryFrame":
        return cls(
            storage=RepositoryStorage(
                environment),
        )

    def save(self, frame: EntityFrame) -> None:
        self.storage.image_save(RepositoryStorageImage(
            name=self.IMAGE_NAME_TEMPLATE.format(
                id=str(frame.id),
                camera_id=frame.camera_id,
                view_id=frame.view_id,
                timestamp=frame.timestamp.isoformat(),
            ),
            image=frame.image,
        ))

    def find_one(self, params: RepositoryFrameFindParams) -> EntityFrame:
        try:
            image = self.storage.image_find_one(RepositoryStorageImageFindOneParams(
                name=str(params.id),
            ))
            id, camera_id, view_id, timestamp = image.name.split(self.SPLIT_PATTERN)
            return EntityFrame(
                id=uuid.UUID(id),
                camera_id=int(camera_id),
                view_id=int(view_id),
                timestamp=datetime.fromisoformat(timestamp),
                image=image.image,
            )
        except RepositoryStorageImageError as e:
            raise RepositoryFrameError(e.message)

    def delete(self, frame: EntityFrame) -> None:
        self.storage.image_delete(RepositoryStorageImageDeleteParams(
            name=self.IMAGE_NAME_TEMPLATE.format(
                id=str(frame.id),
                camera_id=frame.camera_id,
                view_id=frame.view_id,
                timestamp=frame.timestamp.isoformat(),
            ),
        ))
