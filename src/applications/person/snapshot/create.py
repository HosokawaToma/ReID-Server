from repositories.frame_image import RepositoryFrameImage
from repositories.frame_image import RepositoryFrameImagePushQueueError
from domain.frame_image import DomainFrameImage
from PIL import Image
from datetime import datetime
from dataclasses import dataclass
from environment import Environment
from error import Error
from applications import ApplicationBase


@dataclass
class ApplicationPersonSnapshotCreateParams:
    image: Image.Image
    camera_id: int
    view_id: int
    timestamp: datetime

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

    def save(self, params: ApplicationPersonSnapshotCreateParams) -> None:
        frame_image = DomainFrameImage(
            image=params.image,
            camera_id=params.camera_id,
            view_id=params.view_id,
            timestamp=params.timestamp,
        )
        try:
            self.repository_frame_image.save(frame_image)
            self.repository_frame_image.push_person_snapshot_create(frame_image)
        except Error as error:
            raise ApplicationPersonSnapshotCreateError(error) from error
