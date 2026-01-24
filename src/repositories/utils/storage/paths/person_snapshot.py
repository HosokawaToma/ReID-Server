from dataclasses import dataclass
from domain.id import DomainId
from repositories.utils.storage.paths.base import RepositoryUtilStoragePathBase
from typing import ClassVar

@dataclass
class RepositoryUtilStoragePathPersonSnapshot(RepositoryUtilStoragePathBase):
    directory: ClassVar[str] = "person_snapshots"
    id: DomainId

    @property
    def name(self) -> str:
        return str(self.id)
