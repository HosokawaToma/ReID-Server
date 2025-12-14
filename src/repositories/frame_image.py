from repositories import RepositoryStorage
from repositories import RepositoryStorageImage
from repositories import RepositoryStorageImageFindParams
from repositories import RepositoryStorageImageDeleteParams
from error import Error
from domain.frame_image import DomainFrameImage
from environment import Environment
from dataclasses import dataclass
import uuid
from PIL import Image

@dataclass
class RepositoryFrameImageError(Error):
    pass

class RepositoryFrameImage:
    def __init__(self, storage: RepositoryStorage):
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryFrameImage":
        return cls(
            storage=RepositoryStorage.create(
                environment,
                directory="frame_images",
            ),
        )

    def save(self, frame_image: DomainFrameImage) -> None:
        self.storage.image_save(RepositoryStorageImage(
            name=str(frame_image.id),
            image=frame_image.image,
        ))

    def find_image(self, id: uuid.UUID) -> Image.Image:
        return self.storage.image_find_one(RepositoryStorageImageFindParams(
            name=str(id))).image

    def delete(self, frame_image: DomainFrameImage) -> None:
        self.storage.image_delete(RepositoryStorageImageDeleteParams(
            name=str(frame_image.id),
        ))
