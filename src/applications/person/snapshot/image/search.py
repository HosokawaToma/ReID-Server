from dataclasses import dataclass
import uuid
from PIL import Image
from environment import Environment
from repositories.image import RepositoryImage
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
    def __init__(self, repository_image: RepositoryImage):
        self.repository_image = repository_image

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotImageSearch":
        return cls(
            repository_image=RepositoryImage.create(environment),
        )

    def search(self, params: ApplicationPersonSnapshotImageSearchParams) -> ApplicationPersonSnapshotImageSearchItem:
        try:
            return ApplicationPersonSnapshotImageSearchItem(
                image=self.repository_image.find_person_snapshot(params.id).image,
            )
        except Error as error:
            raise ApplicationPersonSnapshotImageSearchError(error) from error
