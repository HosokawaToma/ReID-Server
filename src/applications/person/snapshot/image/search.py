from environment import Environment
from dto.image import DtoImage
from repositories.image import RepositoryImage
from error import Error
from applications import ApplicationBase
from dto.id import DtoId

class ApplicationPersonSnapshotImageSearchError(Error):
    pass

class ApplicationPersonSnapshotImageSearchNotFoundError(ApplicationPersonSnapshotImageSearchError):
    pass

class ApplicationPersonSnapshotImageSearch(ApplicationBase):
    def __init__(self, repository_image: RepositoryImage):
        self.repository_image = repository_image

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotImageSearch":
        return cls(
            repository_image=RepositoryImage.create(environment),
        )

    def search(self, id: DtoId) -> DtoImage:
        try:
            image = self.repository_image.find_person_snapshot(id.id)
            return DtoImage(image=image.image)
        except Error as error:
            raise ApplicationPersonSnapshotImageSearchError(error) from error
