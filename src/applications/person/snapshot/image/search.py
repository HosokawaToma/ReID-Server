from dataclasses import dataclass
import uuid
from PIL import Image
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotError
from domain.person.snapshot import DomainPersonSnapshot
from error import Error

class ApplicationPersonSnapshotImageSearchError(Error):
    pass

@dataclass
class ApplicationPersonSnapshotImageSearchItem:
    image: Image.Image
@dataclass
class ApplicationPersonSnapshotImageSearchParams:
    id: uuid.UUID

class ApplicationPersonSnapshotImageSearch:
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
            if person_snapshot is None:
                raise ApplicationPersonSnapshotImageSearchError(f"Person snapshot not found: {params.id}")
            return ApplicationPersonSnapshotImageSearchItem(image=person_snapshot.find_image(self.repository_person_snapshot))
        except RepositoryPersonSnapshotError as e:
            raise ApplicationPersonSnapshotImageSearchError(e.message)
