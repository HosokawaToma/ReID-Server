"""
人物検出画像検索アプリケーション

人物検出IDでストレージから画像を取得し、DTOで返す。
"""
from environment import Environment
from dto.image import DtoImage
from repositories.image import RepositoryImage
from applications import ApplicationBase
from dto.id import DtoId
from domain.id import DomainId


class ApplicationPersonSnapshotImageSearch(ApplicationBase):
    """
    人物検出画像を検索するアプリケーションクラス。
    """

    def __init__(self, repository_image: RepositoryImage):
        """
        アプリケーションを初期化する。

        :param RepositoryImage repository_image: 画像リポジトリ
        """
        self.repository_image = repository_image

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotImageSearch":
        """
        環境からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return ApplicationPersonSnapshotImageSearch: アプリケーションインスタンス
        """
        return cls(
            repository_image=RepositoryImage.create(environment),
        )

    def search(self, id: DtoId) -> DtoImage:
        """
        人物検出画像を検索する
        :param DtoId id: 人物検出画像のID
        :return DtoImage: 人物検出画像
        :raises ApplicationPersonSnapshotImageSearchError: 人物検出画像検索に失敗した場合に発生するエラー
        """
        image = self.repository_image.find_person_snapshot(DomainId(id=id.id))
        return DtoImage(bytes=image.bytes, format=image.format)
