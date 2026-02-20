"""
バックグラウンドアプリケーション用ユーティリティ基底

環境からインスタンスを生成する抽象基底を定義する。
"""
from environment import Environment
from typing import Type, TypeVar
from abc import ABC, abstractmethod


T = TypeVar("T", bound="BackgroundApplicationUtilsBase")


class BackgroundApplicationUtilsBase(ABC):
    """
    バックグラウンドアプリケーションの抽象基底クラス。

    環境から create でインスタンスを生成する。
    """
    @classmethod
    @abstractmethod
    def create(cls: Type[T], environment: Environment) -> T:
        """
        環境からインスタンスを生成する。サブクラスで実装する。

        :param Environment environment: 環境設定
        :return T: アプリケーションインスタンス
        """
        pass
