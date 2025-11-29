from repositories import RepositoryStorage
from repositories import RepositoryStorageImage
from repositories import StorageImageNotFoundError
from repositories import StorageImageMultipleError
from repositories import StorageImageInvalidError
from repositories import RepositoryStorageImageFindOneParams
from entities.person.snapshot import PersonSnapshotImage
from dataclasses import dataclass
import uuid
from environment import Environment

@dataclass
class RepositoryPersonSnapshotImageFindOneParams:
    id: uuid.UUID

class RepositoryPersonSnapshotImageError(Exception):
    pass

class PersonSnapshotImageNotFoundError(RepositoryPersonSnapshotImageError):
    pass

class PersonSnapshotImageMultipleError(RepositoryPersonSnapshotImageError):
    pass

class PersonSnapshotImageInvalidError(RepositoryPersonSnapshotImageError):
    pass

class RepositoryPersonSnapshotImage:
    def __init__(self, storage: RepositoryStorage):
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshotImage":
        return cls(
            storage=RepositoryStorage(environment),
        )

    def save(self, image: PersonSnapshotImage) -> None:
        self.storage.image_save(RepositoryStorageImage(
            name=str(image.id),
            image=image.image,
        ))

    def find_one(self, params: RepositoryPersonSnapshotImageFindOneParams) -> PersonSnapshotImage:
        try:
            image = self.storage.image_find_one(
                RepositoryStorageImageFindOneParams(
                        name=str(params.id),
                    )
                )
            return PersonSnapshotImage(
                id=params.id,
                image=image.image,
            )
        except StorageImageNotFoundError:
            raise PersonSnapshotImageNotFoundError
        except StorageImageMultipleError:
            raise PersonSnapshotImageMultipleError
        except StorageImageInvalidError:
            raise PersonSnapshotImageInvalidError
