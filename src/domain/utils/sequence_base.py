"""
ドメイン用シーケンス基底クラス

ドメインオブジェクトのリストを保持するシーケンス型の基底。末尾への追加・インデックス参照・長さ取得・イテレーション・同型シーケンスとの結合を提供する。
"""
from abc import ABC
from typing import TypeVar, Generic
from typing_extensions import Self
from domain.utils.base import DomainUtilsBase
from dataclasses import dataclass
from typing import Iterator

T = TypeVar("T", bound=DomainUtilsBase)


@dataclass(frozen=True)
class DomainUtilsSequenceBase(ABC, Generic[T]):
    """
    ドメインオブジェクトのシーケンスの基底クラス。

    要素のリストを保持する。末尾への 1 件追加・要素のインデックス取得・インデックスによる要素取得・長さ・イテレーション・同型のシーケンスとの結合が可能。
    """
    items: list[T]

    def add(self, item: T) -> None:
        """
        末尾に要素を 1 件追加する。破壊的にリストを更新する。

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
        同じ型のシーケンスを末尾に連結した新しいシーケンスを返す。元のインスタンスは変更しない。

        :param Self other: 連結するシーケンス
        :return Self: 連結後の新しいシーケンス
        """
        return self.__class__(items=self.items + other.items)
