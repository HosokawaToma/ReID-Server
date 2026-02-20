"""
YOLO 姿勢推定リポジトリ

姿勢推定モジュールをキャッシュし、ドメイン用にラップして返す。
"""
from modules.yolo.pose_estimator import ModuleYoloPoseEstimator
from domain.yolo.pose_estimator import DomainYoloPoseEstimator
from typing import ClassVar


class RepositoryYoloPoseEstimator:
    """
    YOLO 姿勢推定を提供するリポジトリ。

    モジュールはクラス変数でキャッシュし、find で DomainYoloPoseEstimator として返す。
    """
    CACHE: ClassVar[ModuleYoloPoseEstimator | None] = None

    def __init__(self) -> None:
        """未ロード時はモジュールをロードしてキャッシュする。"""
        if RepositoryYoloPoseEstimator.CACHE is None:
            RepositoryYoloPoseEstimator.CACHE = ModuleYoloPoseEstimator()
        self.model = RepositoryYoloPoseEstimator.CACHE

    @classmethod
    def create(cls) -> "RepositoryYoloPoseEstimator":
        """
        リポジトリインスタンスを生成する。

        :return RepositoryYoloPoseEstimator: リポジトリインスタンス
        """
        return cls()

    def find(self) -> DomainYoloPoseEstimator:
        """
        キャッシュしている姿勢推定をドメイン用にラップして返す。

        :return DomainYoloPoseEstimator: 姿勢推定のドメインラッパー
        """
        return DomainYoloPoseEstimator(model=self.model)
