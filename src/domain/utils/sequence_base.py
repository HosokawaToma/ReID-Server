from abc import ABC
from typing import TypeVar, Generic
from domain.utils.base import DomainUtilsBase
from dataclasses import dataclass
from typing import Iterator
from error import Error

T = TypeVar("T", bound=DomainUtilsBase)


class DomainUtilsSequenceBaseError(Error):
    pass


@dataclass(frozen=True)
class DomainUtilsSequenceBase(ABC, Generic[T]):
    items: list[T]

    def add(self, item: T) -> None:
        self.items.append(item)

    def index(self, item: T) -> int:
        return self.items.index(item)

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, index: int) -> T:
        return self.items[index]

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}([{', '.join(repr(item) for item in self.items)}])"

    def __add__(self, other: "DomainUtilsSequenceBase[T]") -> "DomainUtilsSequenceBase[T]":
        return DomainUtilsSequenceBase(items=self.items + other.items)
