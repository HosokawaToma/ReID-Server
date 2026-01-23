from abc import ABC
from typing import TypeVar, Generic
from domain.utils.base import DomainUtilsBase
from dataclasses import dataclass
from typing import Iterator

T = TypeVar("T", bound=DomainUtilsBase)

@dataclass
class DomainUtilsSequenceBase(ABC, Generic[T]):
    items: list[T]

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> T:
        return self.items[index]

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)
