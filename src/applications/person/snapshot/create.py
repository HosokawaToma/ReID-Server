from repositories.frame_image import RepositoryFrameImage
from dto.image import DtoImage
from dto.frame_image.property import DtoFrameImageProperty
from domain.frame_image import DomainFrameImage
from environment import Environment
from error import Error
from applications import ApplicationBase

class ApplicationPersonSnapshotCreateError(Error):
    pass

class ApplicationPersonSnapshotCreate(ApplicationBase):
    def __init__(
        self,
        repository_frame_image: RepositoryFrameImage,
    ):
        self.repository_frame_image = repository_frame_image

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotCreate":
        return cls(
            repository_frame_image=RepositoryFrameImage.create(
                environment),
        )

    def save(self, image: DtoImage, frame_image_property: DtoFrameImageProperty) -> None:
        domain_frame_image = DomainFrameImage(
            image=image.image,
            camera_id=frame_image_property.camera_id,
            view_id=frame_image_property.view_id,
            timestamp=frame_image_property.timestamp,
        )
        try:
            self.repository_frame_image.save(domain_frame_image)
            self.repository_frame_image.push_person_snapshot_create(domain_frame_image)
        except Error as error:
            raise ApplicationPersonSnapshotCreateError(error) from error
