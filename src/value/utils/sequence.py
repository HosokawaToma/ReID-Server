from value.utils import ValueUtilsBase
from typing import TypeVar, Generic
from typing import Iterator

T = TypeVar("T", bound="ValueUtilsBase")

class ValueUtilsSequenceBase(ValueUtilsBase, Generic[T]):
    items: list[T]

    def __init__(self, items: list[T]):
        self.items = items

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)
