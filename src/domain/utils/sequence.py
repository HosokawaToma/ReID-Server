from domain.utils import DomainUtilsBase
from typing import TypeVar, Generic
from typing import Iterator

T = TypeVar("T", bound="DomainUtilsBase")

class DomainUtilsSequenceBase(DomainUtilsBase, Generic[T]):
    items: list[T]

    def __init__(self, items: list[T]):
        self.items = items

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)
