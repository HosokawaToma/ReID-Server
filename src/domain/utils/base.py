"""
ドメインユーティリティ基底

ドメインモデルの抽象基底クラスを定義する。
"""
from abc import ABC
from dataclasses import dataclass, fields


@dataclass(frozen=True)
class DomainUtilsBase(ABC):
    """
    ドメインモデルの抽象基底クラス。

    すべてのドメインエンティティ・値オブジェクトが継承する。文字列表現はクラス名とフィールド一覧で与える。
    """

    def __repr__(self) -> str:
        """クラス名と全フィールドの値を含む文字列表現を返す。"""
        return f"{self.__class__.__name__}({fields(self)})"
