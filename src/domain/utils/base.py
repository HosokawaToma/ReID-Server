"""
ドメインユーティリティ基底

ドメインモデルの抽象基底クラスとエラーを定義する。
"""
from abc import ABC
from dataclasses import dataclass, fields
from error import Error


class DomainUtilsBaseError(Error):
    """ドメインユーティリティで発生するエラー。"""
    pass


@dataclass(frozen=True)
class DomainUtilsBase(ABC):
    """
    ドメインモデルのベースクラス
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({fields(self)})"
