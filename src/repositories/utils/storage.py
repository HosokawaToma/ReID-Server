from pathlib import Path
from environment import Environment
from PIL import Image
import PIL
from error import Error

class RepositoryUtilStorageError(Error):
    pass

class RepositoryUtilStorageNotFoundError(RepositoryUtilStorageError):
    pass

class RepositoryUtilStoragePermissionError(RepositoryUtilStorageError):
    pass

class RepositoryUtilStorageIsADirectoryError(RepositoryUtilStorageError):
    pass

class RepositoryUtilStorageUnidentifiedImageError(RepositoryUtilStorageError):
    pass

class RepositoryUtilStorageDecompressionBombError(RepositoryUtilStorageError):
    pass

class RepositoryUtilStorageOSError(RepositoryUtilStorageError):
    pass

class RepositoryUtilStorageMultipleError(RepositoryUtilStorageError):
    pass

class RepositoryUtilStorage:
    """
    ストレージ操作に関するユーティリティを集約する
    :param Path path: ストレージディレクトリ
    """
    IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "webp"]

    def __init__(self, path: Path):
        self.path = path

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryUtilStorage":
        return cls(
            path=environment.storage_directory,
        )

    def search_image(self, name: str, directory: Path) -> Path:
        """
        ストレージ内の画像を検索する
        :param str name: 画像名（拡張子なし）
        :param Path directory: 検索対象ディレクトリ
        :return Path: 画像パス
        :raise RepositoryUtilStorageNotFoundError: 画像が見つからない場合
        :raise RepositoryUtilStorageMultipleError: 画像が複数見つかった場合
        """
        match_file_names: list[Path] = []
        for extension in self.IMAGE_EXTENSIONS:
            file_path = self.path / directory / f"{name}.{extension}"
            if file_path.exists():
                match_file_names.append(file_path)
        if len(match_file_names) == 0:
            raise RepositoryUtilStorageNotFoundError()
        if len(match_file_names) > 1:
            raise RepositoryUtilStorageMultipleError()
        return match_file_names[0]

    def open_image(self, path: Path) -> Image.Image:
        """
        画像を開く
        :param Path path: 画像パス
        :return Image.Image: 画像
        :raise RepositoryUtilStorageNotFoundError: 画像が見つからない場合
        :raise RepositoryUtilStoragePermissionError: 画像にアクセスできない場合
        :raise RepositoryUtilStorageIsADirectoryError: 画像がディレクトリの場合
        :raise RepositoryUtilStorageUnidentifiedImageError: 画像が不明な形式の場合
        :raise RepositoryUtilStorageDecompressionBombError: 画像が圧縮爆弾の場合
        :raise RepositoryUtilStorageOSError: 画像を読み込めない場合
        """
        try:
            return Image.open(path)
        except FileNotFoundError as error:
            raise RepositoryUtilStorageNotFoundError(error) from error
        except PermissionError as error:
            raise RepositoryUtilStoragePermissionError(error) from error
        except IsADirectoryError as error:
            raise RepositoryUtilStorageIsADirectoryError(error) from error
        except PIL.UnidentifiedImageError as error:
            raise RepositoryUtilStorageUnidentifiedImageError(error) from error
        except Image.DecompressionBombError as error:
            raise RepositoryUtilStorageDecompressionBombError(error) from error
        except OSError as error:
            raise RepositoryUtilStorageOSError(error) from error
