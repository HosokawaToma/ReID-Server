"""
YOLO インスタンスセグメンテーションリポジトリ

セグメンテーションモジュールをキャッシュし、ドメイン用にラップして返す。
"""
from modules.yolo.instance_segmenter import ModuleYoloInstanceSegmenter
from domain.yolo.instance_segmenter import DomainYoloInstanceSegmenter
from typing import ClassVar


class RepositoryYoloInstanceSegmenter:
    """
    YOLO インスタンスセグメンテーションを提供するリポジトリ。

    モジュールはクラス変数でキャッシュし、find で DomainYoloInstanceSegmenter として返す。
    """
    CACHE: ClassVar[ModuleYoloInstanceSegmenter | None] = None

    def __init__(self) -> None:
        """未ロード時はモジュールをロードしてキャッシュする。"""
        if RepositoryYoloInstanceSegmenter.CACHE is None:
            RepositoryYoloInstanceSegmenter.CACHE = ModuleYoloInstanceSegmenter()
        self.model = RepositoryYoloInstanceSegmenter.CACHE

    @classmethod
    def create(cls) -> "RepositoryYoloInstanceSegmenter":
        """
        リポジトリインスタンスを生成する。

        :return RepositoryYoloInstanceSegmenter: リポジトリインスタンス
        """
        return cls()

    def find(self) -> DomainYoloInstanceSegmenter:
        """
        キャッシュしているセグメンテーションをドメイン用にラップして返す。

        :return DomainYoloInstanceSegmenter: セグメンテーションのドメインラッパー
        """
        return DomainYoloInstanceSegmenter(model=self.model)
