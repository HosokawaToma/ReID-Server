from dataclasses import dataclass
import uuid
from PIL import Image
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from error import Error
from applications import ApplicationBase

class ApplicationPersonSnapshotImageSearchError(Error):
    pass

class ApplicationPersonSnapshotImageSearchNotFoundError(ApplicationPersonSnapshotImageSearchError):
    pass

@dataclass
class ApplicationPersonSnapshotImageSearchItem:
    image: Image.Image
@dataclass
class ApplicationPersonSnapshotImageSearchParams:
    id: uuid.UUID

class ApplicationPersonSnapshotImageSearch(ApplicationBase):
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotImageSearch":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
        )

    def search(self, params: ApplicationPersonSnapshotImageSearchParams) -> ApplicationPersonSnapshotImageSearchItem:
        try:
            person_snapshot = self.repository_person_snapshot.find_first(filters=RepositoryPersonSnapshotFilters(ids=[params.id]))
        except Error as error:
            raise ApplicationPersonSnapshotImageSearchError(error) from error
        if person_snapshot is None:
            raise ApplicationPersonSnapshotImageSearchNotFoundError()
        return ApplicationPersonSnapshotImageSearchItem(image=person_snapshot.image)
