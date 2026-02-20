"""
ストレージパスの基底

画像のディレクトリとファイル名を表す抽象基底を定義する。
"""
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import ClassVar


@dataclass
class RepositoryUtilStoragePathBase(ABC):
    """
    ストレージ内の画像パスの抽象基底クラス。

    サブクラスは directory と name を定義する。
    """
    directory: ClassVar[str]

    @property
    @abstractmethod
    def name(self) -> str:
        """
        ファイル名（拡張子なし）を返す。サブクラスで実装する。

        :return str: ファイル名
        """
        pass
