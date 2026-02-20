"""
ReID モデルリポジトリ

ReID モデルをクラスキャッシュで保持し、ドメイン用にラップして返す。
"""
from typing import ClassVar
from modules.reid.model import ModuleReIDModel
from domain.reid.model import DomainReIDModel


class RepositoryReID:
    """
    ReID モデルを提供するリポジトリクラス。

    モデルはクラス変数でキャッシュし、find で DomainReIDModel として返す。
    """
    CACHE: ClassVar[ModuleReIDModel | None] = None

    def __init__(self) -> None:
        """
        リポジトリを初期化する。未ロード時はモデルをロードしてキャッシュする。
        """
        if RepositoryReID.CACHE is None:
            RepositoryReID.CACHE = ModuleReIDModel()
        self.model = RepositoryReID.CACHE

    @classmethod
    def create(cls) -> "RepositoryReID":
        """
        リポジトリインスタンスを生成する。

        :return RepositoryReID: リポジトリインスタンス
        """
        return cls()

    def find(self) -> DomainReIDModel:
        """
        キャッシュしている ReID モデルをドメイン用にラップして返す。

        :return DomainReIDModel: ReID モデルのドメインラッパー
        """
        return DomainReIDModel(model=self.model)
