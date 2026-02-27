"""
カメラフレーム画像検索アプリケーション。

カメラフレーム ID を受け取り、対応する画像を表す DTO を返す。
"""
from repositories.image import RepositoryImage
from domain.id import DomainId
from environment import Environment
from dto.image import DtoImage
from dto.id import DtoId
from applications import ApplicationBase


class ApplicationCameraFrameImageSearch(ApplicationBase):
    """
    カメラフレーム画像検索を行うアプリケーションクラス。
    """

    def __init__(self, repository_image: RepositoryImage):
        """
        アプリケーションを初期化する。

        :param RepositoryImage repository_image: 画像リポジトリ
        """
        self.repository_image = repository_image

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationCameraFrameImageSearch":
        """
        環境変数からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境変数
        :return ApplicationCameraFrameImageSearch: アプリケーションインスタンス
        """
        return cls(
            repository_image=RepositoryImage.create(environment),
        )

    def search(self, id: DtoId) -> DtoImage:
        """
        指定した ID に紐づくカメラフレーム画像を検索し、画像 DTO を返す。

        :param DtoId id: カメラフレーム画像の ID
        :return DtoImage: 画像のバイト列とフォーマット
        :raises NotFoundError: 画像が存在しない、または読み込めない場合
        :raises ConflictError: 同一 ID で複数拡張子のファイルが存在する場合
        :raises InternalServerError: 画像の取得に失敗した場合
        """
        image = self.repository_image.find_camera_frame(DomainId(id=id.id))
        return DtoImage(bytes=image.bytes, format=image.format)
