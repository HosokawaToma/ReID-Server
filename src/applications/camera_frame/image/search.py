from repositories.image import RepositoryImage
from domain.id import DomainId
from environment import Environment
from dto.image import DtoImage
from dto.id import DtoId
from applications import ApplicationBase

class ApplicationCameraFrameImageSearch(ApplicationBase):
    def __init__(self, repository_image: RepositoryImage):
        self.repository_image = repository_image

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationCameraFrameImageSearch":
        return cls(
            repository_image=RepositoryImage.create(environment),
        )

    def search(self, id: DtoId) -> DtoImage:
        image = self.repository_image.find_camera_frame(DomainId(id=id.id))
        return DtoImage(image=image.image, format=image.format)
