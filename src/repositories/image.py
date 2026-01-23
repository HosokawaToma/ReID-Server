from repositories.utils.storage import RepositoryUtilStorage
from repositories.utils.storage.paths.camera_frame import RepositoryUtilStoragePathCameraFrame
from repositories.utils.storage.paths.person_snapshot import RepositoryUtilStoragePathPersonSnapshot
from environment import Environment
from domain.image import DomainImage
from domain.id import DomainId
from error import Error

class RepositoryImageError(Error):
    pass

class RepositoryImage:
    def __init__(self, storage: RepositoryUtilStorage):
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryImage":
        return cls(storage=RepositoryUtilStorage.create(environment))

    def find_camera_frame(self, id: DomainId) -> DomainImage:
        return self.storage.search_image(RepositoryUtilStoragePathCameraFrame(id=id))

    def find_person_snapshot(self, id: DomainId) -> DomainImage:
        return self.storage.search_image(RepositoryUtilStoragePathPersonSnapshot(id=id))
