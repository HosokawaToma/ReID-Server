from repositories.image import RepositoryImage
from environment import Environment
from dto.image import DtoImage
import uuid
from applications import ApplicationBase

class ApplicationFrameImageSearch(ApplicationBase):
    def __init__(self, repository_image: RepositoryImage):
        self.repository_image = repository_image

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationFrameImageSearch":
        return cls(
            repository_image=RepositoryImage.create(environment),
        )

    def search(self, id: uuid.UUID) -> DtoImage:
        return DtoImage(image=self.repository_image.find_frame(id).image)
