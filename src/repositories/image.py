"""
画像リポジトリ

カメラフレーム・人物検出の画像をストレージから取得する。
"""
from repositories.utils.storage import RepositoryUtilStorage
from repositories.utils.storage.paths.camera_frame import RepositoryUtilStoragePathCameraFrame
from repositories.utils.storage.paths.person_snapshot import RepositoryUtilStoragePathPersonSnapshot
from environment import Environment
from domain.image import DomainImage
from domain.id import DomainId
from error import Error


class RepositoryImageError(Error):
    """画像リポジトリで発生するエラー。"""
    pass


class RepositoryImage:
    """
    画像の取得を行うリポジトリクラス。

    カメラフレーム画像と人物検出画像をストレージパス経由で取得する。
    """

    def __init__(self, storage: RepositoryUtilStorage):
        """
        リポジトリを初期化する。

        :param RepositoryUtilStorage storage: ストレージユーティリティ
        """
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryImage":
        """
        環境からリポジトリインスタンスを生成する。

        :param Environment environment: 環境設定
        :return RepositoryImage: リポジトリインスタンス
        """
        return cls(storage=RepositoryUtilStorage.create(environment))

    def find_camera_frame(self, id: DomainId) -> DomainImage:
        """
        カメラフレームIDで画像を取得する。

        :param DomainId id: カメラフレームID
        :return DomainImage: 画像
        :raises NotFoundError: 画像が存在しない場合
        """
        return self.storage.search_image(RepositoryUtilStoragePathCameraFrame(id=id))

    def find_person_snapshot(self, id: DomainId) -> DomainImage:
        """
        人物検出IDで画像を取得する。

        :param DomainId id: 人物検出結果ID
        :return DomainImage: 画像
        :raises NotFoundError: 画像が存在しない場合
        """
        return self.storage.search_image(RepositoryUtilStoragePathPersonSnapshot(id=id))
