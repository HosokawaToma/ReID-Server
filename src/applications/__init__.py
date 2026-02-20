"""
アプリケーション層の基底

環境に依存するアプリケーションの抽象基底クラスを定義する。
"""
from environment import Environment
from typing import Type, TypeVar
from abc import ABC, abstractmethod


T = TypeVar("T", bound="ApplicationBase")


class ApplicationBase(ABC):
    """
    アプリケーションの抽象基底クラス。

    サブクラスは create を実装し、環境からインスタンスを生成する。
    """
    @classmethod
    @abstractmethod
    def create(cls: Type[T], environment: Environment) -> T:
        """
        環境からアプリケーションインスタンスを生成する。サブクラスで実装する。

        :param Environment environment: 環境設定
        :return T: アプリケーションインスタンス
        """
        pass
