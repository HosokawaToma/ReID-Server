from dataclasses import dataclass
from domain.id import DomainId
from repositories.utils.storage.paths.base import RepositoryUtilStoragePathBase
from typing import ClassVar

@dataclass
class RepositoryUtilStoragePathCameraFrame(RepositoryUtilStoragePathBase):
    directory: ClassVar[str] = "camera_frame_images"
    id: DomainId

    @property
    def name(self) -> str:
        return str(self.id)
