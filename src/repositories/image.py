from repositories.utils.storage import RepositoryUtilStorage
from domain.image import DomainImage
from environment import Environment
from error import Error
from pathlib import Path
import uuid

class RepositoryImageError(Error):
    pass

class RepositoryImageFindPersonSnapshotError(RepositoryImageError):
    pass

class RepositoryImageFindFrameError(RepositoryImageError):
    pass

class RepositoryImage:
    def __init__(self, storage: RepositoryUtilStorage):
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryImage":
        return cls(
            storage=RepositoryUtilStorage.create(
                environment,
            ),
        )

    def find_person_snapshot(self, id: uuid.UUID) -> DomainImage:
        try:
            image = self.storage.search_image(str(id), Path("person_snapshots"))
            return DomainImage(image=self.storage.open_image(image))
        except Error as error:
            raise RepositoryImageFindPersonSnapshotError(error) from error

    def find_frame(self, id: uuid.UUID) -> DomainImage:
        try:
            image = self.storage.search_image(str(id), Path("frames"))
            return DomainImage(image=self.storage.open_image(image))
        except Error as error:
            raise RepositoryImageFindFrameError(error) from error
