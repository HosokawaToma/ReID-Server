from repositories.frame_image import RepositoryFrameImage
from environment import Environment
from dto.frame_image import DtoFrameImage
import uuid
from domain.frame_image.filter import DomainFrameImageFilter
from applications import ApplicationBase

class ApplicationFrameImageSearch(ApplicationBase):
    def __init__(self, repository_frame_image: RepositoryFrameImage):
        self.repository_frame_image = repository_frame_image

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationFrameImageSearch":
        return cls(
            repository_frame_image=RepositoryFrameImage.create(environment),
        )

    def search(self, id: uuid.UUID) -> DtoFrameImage:
        image = self.repository_frame_image.find_first(
            filters=DomainFrameImageFilter(
                ids=[id],
            ),
        )
        return DtoFrameImage(
            id=image.id,
            camera_id=image.camera_id,
            view_id=image.view_id,
            timestamp=image.timestamp,
            image=image.image,
        )
