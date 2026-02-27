"""
アプリケーション層の基底。

ユースケースを実行するアプリケーションクラスが継承する抽象基底であり、
環境設定に基づいて必要な依存（リポジトリなど）を組み立てたインスタンスを生成する役割を持つ。
"""
from environment import Environment
from typing import Type, TypeVar
from abc import ABC, abstractmethod


T = TypeVar("T", bound="ApplicationBase")


class ApplicationBase(ABC):
    """
    アプリケーションの抽象基底クラス。

    各ユースケース（人物検出作成・検索・正解ラベル割り当て等）はこのサブクラスとして定義する。
    環境設定から必要な依存関係を解決し、ユースケースを実行可能なインスタンスを返す仕様とする。
    プレゼンテーション層は、環境変数から生成したインスタンスの操作を呼び出す。
    """
    @classmethod
    @abstractmethod
    def create(cls: Type[T], environment: Environment) -> T:
        """
        環境変数からアプリケーションインスタンスを生成する。サブクラスで実装する。

        実装では環境変数を参照して必要な依存（リポジトリなど）を組み立て、ユースケースを実行可能なインスタンスを返す。

        :param Environment environment: アプリケーションの動作に必要な環境設定
        :return T: 依存が注入されたアプリケーションインスタンス
        """
        pass
