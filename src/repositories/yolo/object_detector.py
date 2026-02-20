"""
YOLO 物体検出リポジトリ

物体検出モジュールをキャッシュし、ドメイン用にラップして返す。
"""
from modules.yolo.object_detector import ModuleYoloObjectDetector
from domain.yolo.object_detector import DomainYoloObjectDetector
from typing import ClassVar


class RepositoryYoloObjectDetector:
    """
    YOLO 物体検出を提供するリポジトリ。

    モジュールはクラス変数でキャッシュし、find で DomainYoloObjectDetector として返す。
    """
    CACHE: ClassVar[ModuleYoloObjectDetector | None] = None

    def __init__(self) -> None:
        """未ロード時はモジュールをロードしてキャッシュする。"""
        if RepositoryYoloObjectDetector.CACHE is None:
            RepositoryYoloObjectDetector.CACHE = ModuleYoloObjectDetector()
        self.model = RepositoryYoloObjectDetector.CACHE

    @classmethod
    def create(cls) -> "RepositoryYoloObjectDetector":
        """
        リポジトリインスタンスを生成する。

        :return RepositoryYoloObjectDetector: リポジトリインスタンス
        """
        return cls()

    def find(self) -> DomainYoloObjectDetector:
        """
        キャッシュしている物体検出をドメイン用にラップして返す。

        :return DomainYoloObjectDetector: 物体検出のドメインラッパー
        """
        return DomainYoloObjectDetector(model=self.model)
