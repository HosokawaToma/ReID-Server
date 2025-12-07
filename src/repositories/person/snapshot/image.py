from repositories import RepositoryStorage
from repositories import RepositoryStorageImage
from repositories import RepositoryStorageImageFindOneParams
from repositories import RepositoryStorageImageError
from repositories import RepositoryStorageImageDeleteParams
from entities.person.snapshot import EntityPersonSnapshotImage
from dataclasses import dataclass
import uuid
from environment import Environment
from error import Error

@dataclass
class RepositoryPersonSnapshotImageFindOneParams:
    id: uuid.UUID

@dataclass
class RepositoryPersonSnapshotImageDeleteParams:
    id: uuid.UUID

class RepositoryPersonSnapshotImageError(Error):
    pass

class RepositoryPersonSnapshotImage:
    def __init__(self, storage: RepositoryStorage):
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshotImage":
        return cls(
            storage=RepositoryStorage(environment),
        )

    def save(self, image: EntityPersonSnapshotImage) -> None:
        self.storage.image_save(RepositoryStorageImage(
            name=str(image.id),
            image=image.image,
        ))

    def find_one(self, params: RepositoryPersonSnapshotImageFindOneParams) -> EntityPersonSnapshotImage:
        try:
            image = self.storage.image_find_one(
                RepositoryStorageImageFindOneParams(
                        name=str(params.id),
                    )
                )
            return EntityPersonSnapshotImage(
                id=params.id,
                image=image.image,
            )
        except RepositoryStorageImageError as e:
            raise RepositoryPersonSnapshotImageError(e.message)

    def delete(self, params: RepositoryPersonSnapshotImageDeleteParams) -> None:
        try:
            self.storage.image_delete(RepositoryStorageImageDeleteParams(
                name=str(params.id),
            ))
        except RepositoryStorageImageError as e:
            raise RepositoryPersonSnapshotImageError(e.message)
