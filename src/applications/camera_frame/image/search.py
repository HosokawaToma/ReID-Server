"""
カメラフレーム画像検索アプリケーション

カメラフレームIDでストレージから画像を取得し、DTOで返す。
"""
from repositories.image import RepositoryImage
from domain.id import DomainId
from environment import Environment
from dto.image import DtoImage
from dto.id import DtoId
from applications import ApplicationBase


class ApplicationCameraFrameImageSearch(ApplicationBase):
    """
    カメラフレーム画像を検索するアプリケーションクラス。
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
        環境からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return ApplicationCameraFrameImageSearch: アプリケーションインスタンス
        """
        return cls(
            repository_image=RepositoryImage.create(environment),
        )

    def search(self, id: DtoId) -> DtoImage:
        """
        カメラフレーム画像を検索する
        :param DtoId id: カメラフレーム画像のID
        :return DtoImage: カメラフレーム画像
        :raises ApplicationCameraFrameImageSearchError: カメラフレーム画像検索に失敗した場合に発生するエラー
        """
        image = self.repository_image.find_camera_frame(DomainId(id=id.id))
        return DtoImage(bytes=image.bytes, format=image.format)
