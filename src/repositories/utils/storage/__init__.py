"""
ストレージユーティリティ

画像の検索・保存をストレージディレクトリに対して行う。
"""
from pathlib import Path
from environment import Environment
from PIL import Image
import PIL
from error import InternalServerError
from error import NotFoundError, ConflictError
from domain.image import DomainImage
from repositories.utils.storage.paths.base import RepositoryUtilStoragePathBase


class RepositoryUtilStorage:
    """
    ストレージ操作を扱うユーティリティクラス。

    画像の検索（search_image）と保存（save_image）を提供する。
    """

    def __init__(self, path: Path):
        """
        ストレージを初期化する。

        :param Path path: ストレージのルートディレクトリ
        """
        self.path = path

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryUtilStorage":
        """
        環境からストレージユーティリティインスタンスを生成する。

        :param Environment environment: 環境設定
        :return RepositoryUtilStorage: ストレージユーティリティインスタンス
        """
        return cls(
            path=environment.storage_directory,
        )

    def search_image(self, path: RepositoryUtilStoragePathBase) -> DomainImage:
        """
        ストレージ内の画像を検索する
        :param RepositoryUtilStoragePathBase path: 画像パス
        :return DomainImage: 画像
        :raise RepositoryUtilStorageNotFoundError: 画像が見つからない場合
        :raise RepositoryUtilStorageMultipleError: 画像が複数見つかった場合
        """
        extension_list: list[str] = []
        for extension in DomainImage.EXTENSIONS:
            file_path = self.path / path.directory / f"{path.name}.{extension}"
            if file_path.exists():
                extension_list.append(extension)
        if len(extension_list) == 0:
            raise NotFoundError("画像が見つかりません")
        if len(extension_list) > 1:
            raise ConflictError("画像が複数見つかりました")
        try:
            image = Image.open(self.path / path.directory /
                               f"{path.name}.{extension_list[0]}")
            return DomainImage.from_image(image)
        except FileNotFoundError as error:
            raise NotFoundError("画像が見つかりません") from error
        except PermissionError as error:
            raise InternalServerError("画像にアクセスできません") from error
        except IsADirectoryError as error:
            raise InternalServerError("画像がディレクトリの場合") from error
        except PIL.UnidentifiedImageError as error:
            raise InternalServerError("画像が不明な形式の場合") from error
        except Image.DecompressionBombError as error:
            raise InternalServerError("画像が圧縮爆弾の場合") from error
        except OSError as error:
            raise InternalServerError("画像を読み込めない場合") from error

    def save_image(
        self,
        image: DomainImage,
        path: RepositoryUtilStoragePathBase,
    ) -> None:
        """
        画像をストレージに保存する。

        :param DomainImage image: 保存する画像
        :param RepositoryUtilStoragePathBase path: 保存先パス
        :raises InternalServerError: 保存に失敗した場合
        """
        try:
            image.image.save(self.path / path.directory /
                             f"{path.name}.{image.format}")
        except ValueError as error:
            raise InternalServerError("画像を保存できません") from error
        except OSError as error:
            raise InternalServerError("画像を保存できません") from error
