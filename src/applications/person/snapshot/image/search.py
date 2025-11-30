from dataclasses import dataclass
import uuid
from environment import Environment
from repositories.person.snapshot.image import RepositoryPersonSnapshotImage
from repositories.person.snapshot.image import RepositoryPersonSnapshotImageFindOneParams
from repositories.person.snapshot.image import RepositoryPersonSnapshotImageError
from entities.person.snapshot import EntityPersonSnapshotImage

class ApplicationPersonSnapshotImageSearchError(Exception):
    pass

class ApplicationPersonSnapshotImageSearchNotFoundError(ApplicationPersonSnapshotImageSearchError):
    pass

@dataclass
class ApplicationPersonSnapshotImageSearchParams:
    image_id: uuid.UUID

class ApplicationPersonSnapshotImageSearch:
    def __init__(self, repository_person_snapshot_image: RepositoryPersonSnapshotImage):
        self.repository_person_snapshot_image = repository_person_snapshot_image

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotImageSearch":
        return cls(
            repository_person_snapshot_image=RepositoryPersonSnapshotImage.create(environment),
        )

    def search(self, params: ApplicationPersonSnapshotImageSearchParams) -> EntityPersonSnapshotImage:
        try:
            return self.repository_person_snapshot_image.find_one(params=RepositoryPersonSnapshotImageFindOneParams(id=params.image_id))
        except RepositoryPersonSnapshotImageError:
            raise ApplicationPersonSnapshotImageSearchNotFoundError
