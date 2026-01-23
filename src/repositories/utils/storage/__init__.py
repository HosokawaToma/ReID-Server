from pathlib import Path
from environment import Environment
from PIL import Image
import PIL
from error import Error
from domain.image import DomainImage
from repositories.utils.storage.paths.base import RepositoryUtilStoragePathBase

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

class RepositoryUtilStorageInvalidFormatError(RepositoryUtilStorageError):
    pass

class RepositoryUtilStorageInvalidSaveError(RepositoryUtilStorageError):
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

    def search_image(self, path: RepositoryUtilStoragePathBase) -> DomainImage:
        """
        ストレージ内の画像を検索する
        :param RepositoryUtilStoragePathBase path: 画像パス
        :return DomainImage: 画像
        :raise RepositoryUtilStorageNotFoundError: 画像が見つからない場合
        :raise RepositoryUtilStorageMultipleError: 画像が複数見つかった場合
        """
        extension_list: list[str] = []
        for extension in self.IMAGE_EXTENSIONS:
            file_path = self.path / path.directory / f"{path.name}.{extension}"
            if file_path.exists():
                extension_list.append(extension)
        if len(extension_list) == 0:
            raise RepositoryUtilStorageNotFoundError()
        if len(extension_list) > 1:
            raise RepositoryUtilStorageMultipleError()
        try:
            image = Image.open(self.path / path.directory / f"{path.name}.{extension_list[0]}")
            return DomainImage.from_image(image)
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

    def save_image(
        self,
        image: DomainImage,
        path: RepositoryUtilStoragePathBase,
    ) -> None:
        try:
            if image.image.format is None:
                raise RepositoryUtilStorageInvalidFormatError()
            image.image.save(self.path / path.directory / f"{path.name}.{image.image.format}")
        except ValueError as error:
            raise RepositoryUtilStorageInvalidSaveError(error) from error
        except OSError as error:
            raise RepositoryUtilStorageInvalidSaveError(error) from error
