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
    人物検出画像の取得を担当するアプリケーション。

    人物検出結果IDを指定し、ストレージから画像を読み出して画像DTO（バイト列・フォーマット）で返す。
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
        環境変数からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境変数
        :return ApplicationPersonSnapshotImageSearch: アプリケーションインスタンス
        """
        return cls(
            repository_image=RepositoryImage.create(environment),
        )

    def search(self, id: DtoId) -> DtoImage:
        """
        指定した人物検出結果IDに紐づく画像をストレージから取得し、画像DTOで返す。

        :param DtoId id: 人物検出結果のID（画像のキー）
        :return DtoImage: 画像のバイト列とフォーマット
        :raises NotFoundError: 画像が存在しない、または読み込めない場合
        :raises ConflictError: 同一 ID で複数拡張子のファイルが存在する場合
        :raises InternalServerError: ストレージアクセス等で取得に失敗した場合
        """
        image = self.repository_image.find_person_snapshot(DomainId(id=id.id))
        return DtoImage(bytes=image.bytes, format=image.format)
