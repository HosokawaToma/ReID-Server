"""
ドメイン用シーケンス基底クラス

要素のリストを保持するシーケンス型の基底。add/index/len/getitem/iter/add を提供する。
"""
from abc import ABC
from typing import TypeVar, Generic
from typing_extensions import Self
from domain.utils.base import DomainUtilsBase
from dataclasses import dataclass
from typing import Iterator
from error import Error

T = TypeVar("T", bound=DomainUtilsBase)


class DomainUtilsSequenceBaseError(Error):
    """
    シーケンス基底で発生するエラー。
    """
    pass


@dataclass(frozen=True)
class DomainUtilsSequenceBase(ABC, Generic[T]):
    """
    ドメインオブジェクトのシーケンスの基底クラス。

    要素のリストを保持し、追加・参照・結合などの操作を提供する。
    """
    items: list[T]

    def add(self, item: T) -> None:
        """
        末尾に要素を1件追加する。

        :param T item: 追加する要素
        """
        self.items.append(item)

    def index(self, item: T) -> int:
        """
        要素のインデックスを返す。

        :param T item: 検索する要素
        :return int: インデックス
        """
        return self.items.index(item)

    def __len__(self) -> int:
        """要素数を返す。"""
        return len(self.items)

    def __getitem__(self, index: int) -> T:
        """
        インデックスで要素を取得する。

        :param int index: インデックス
        :return T: 要素
        """
        return self.items[index]

    def __iter__(self) -> Iterator[T]:
        """要素のイテレータを返す。"""
        return iter(self.items)

    def __repr__(self) -> str:
        """文字列表現を返す。"""
        return f"{self.__class__.__name__}([{', '.join(repr(item) for item in self.items)}])"

    def __add__(self, other: Self) -> Self:
        """
        別のシーケンスと結合した新しいシーケンスを返す。

        :param Self other: 結合するシーケンス
        :return Self: 結合後の新しいシーケンス
        """
        return self.__class__(items=self.items + other.items)
