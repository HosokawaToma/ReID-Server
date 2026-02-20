"""
アプリケーション層の基底

ユースケースを実行するアプリケーションクラスが継承する抽象基底。
環境（DB・Redis・ストレージ等の接続情報）に依存するため、インスタンス生成は環境を渡して行い、環境に応じたリポジトリ等を組み立てる。
"""
from environment import Environment
from typing import Type, TypeVar
from abc import ABC, abstractmethod


T = TypeVar("T", bound="ApplicationBase")


class ApplicationBase(ABC):
    """
    アプリケーションの抽象基底クラス。

    各ユースケース（人物検出作成・検索・正解ラベル割り当て等）はこのサブクラスとして定義する。
    環境から接続先やパスを読み取り、必要なリポジトリを組み立てたインスタンスを返す仕様とする。
    プレゼンテーション層は、環境から生成したインスタンスの操作を呼び出す。
    """
    @classmethod
    @abstractmethod
    def create(cls: Type[T], environment: Environment) -> T:
        """
        環境設定からアプリケーションインスタンスを生成する。サブクラスで実装する。

        実装では環境の DB・Redis・ストレージ等の設定を参照し、必要なリポジトリを組み立てて保持したインスタンスを返す。

        :param Environment environment: 環境設定（DB・Redis・ストレージ等）
        :return T: 依存が注入されたアプリケーションインスタンス
        """
        pass
