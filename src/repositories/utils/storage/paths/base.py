from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import ClassVar

@dataclass
class RepositoryUtilStoragePathBase(ABC):
    directory: ClassVar[str]

    @property
    @abstractmethod
    def name(self) -> str:
        pass
