"""
画像リポジトリ

カメラフレーム画像・人物スナップショット画像を、ストレージ上の論理パス（ID に紐づく）から取得する。
ストレージへの実際のアクセスはストレージユーティリティに委譲する。
"""
from repositories.utils.storage import RepositoryUtilStorage
from repositories.utils.storage.paths.camera_frame import RepositoryUtilStoragePathCameraFrame
from repositories.utils.storage.paths.person_snapshot import RepositoryUtilStoragePathPersonSnapshot
from environment import Environment
from domain.image import DomainImage
from domain.id import DomainId
from error import Error


class RepositoryImageError(Error):
    """画像リポジトリ層で発生するエラー（継承用）。"""
    pass


class RepositoryImage:
    """
    画像の取得を担当するリポジトリ。

    カメラフレーム画像は「frame_images / ID」、人物スナップショット画像は「person_snapshots / ID」という論理パスでストレージを検索する。
    該当ファイルが無い、または同一 ID で複数拡張子が存在する場合はストレージが NotFoundError / ConflictError を送出する。
    """

    def __init__(self, storage: RepositoryUtilStorage):
        """
        利用するストレージユーティリティを設定する。

        :param RepositoryUtilStorage storage: 画像の検索に使うストレージ
        """
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryImage":
        """
        環境に定義されたストレージディレクトリからインスタンスを生成する。

        :param Environment environment: 環境設定
        :return RepositoryImage: リポジトリインスタンス
        """
        return cls(storage=RepositoryUtilStorage.create(environment))

    def find_camera_frame(self, id: DomainId) -> DomainImage:
        """
        カメラフレーム ID に対応する画像をストレージから 1 件取得する。

        論理パスは「frame_images / 当該 ID」に対応する。該当ファイルが無い・複数拡張子が存在する場合は NotFoundError または ConflictError。

        :param DomainId id: カメラフレームの一意 ID
        :return DomainImage: 取得した画像
        :raises NotFoundError: 画像が存在しない、または読み込めない場合
        :raises ConflictError: 同一 ID で複数拡張子のファイルが存在する場合
        """
        return self.storage.search_image(RepositoryUtilStoragePathCameraFrame(id=id))

    def find_person_snapshot(self, id: DomainId) -> DomainImage:
        """
        人物スナップショット ID に対応する画像をストレージから 1 件取得する。

        論理パスは「person_snapshots / 当該 ID」に対応する。取得条件・例外はカメラフレーム画像と同様。

        :param DomainId id: 人物スナップショットの一意 ID
        :return DomainImage: 取得した画像
        :raises NotFoundError: 画像が存在しない、または読み込めない場合
        :raises ConflictError: 同一 ID で複数拡張子のファイルが存在する場合
        """
        return self.storage.search_image(RepositoryUtilStoragePathPersonSnapshot(id=id))
