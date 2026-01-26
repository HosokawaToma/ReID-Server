from typing import ClassVar
from modules.reid.model import ModuleReIDModel
from domain.reid.model import DomainReIDModel

class RepositoryReID:
    CACHE: ClassVar[ModuleReIDModel | None] = None

    def __init__(self):
        if RepositoryReID.CACHE is None:
            RepositoryReID.CACHE = ModuleReIDModel()
        self.model = RepositoryReID.CACHE

    @classmethod
    def create(cls) -> "RepositoryReID":
        return cls()

    def find(self) -> DomainReIDModel:
        return DomainReIDModel(model=self.model)
