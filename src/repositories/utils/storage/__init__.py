"""
ストレージユーティリティ

ファイルシステム上のストレージルートを基準に、画像の検索・保存を行う。
パスは「ディレクトリ名 + ファイル名（拡張子なし）」で表現し、対応する拡張子（jpg / jpeg / png）の有無で検索する。
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
    ストレージ操作を担当するユーティリティ。

    ルート直下に「ディレクトリ名 / ファイル名.拡張子」で画像を配置する想定。
    検索時は jpg / jpeg / png の順で存在する拡張子を探し、0 件なら NotFoundError、2 種類以上なら ConflictError となる。
    保存時は画像のフォーマットを拡張子として用いる。
    """

    def __init__(self, path: Path):
        """
        ストレージのルートディレクトリを設定する。

        :param Path path: 画像を格納するルート（絶対パス推奨）
        """
        self.path = path

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryUtilStorage":
        """
        環境に定義されたストレージディレクトリからインスタンスを生成する。

        :param Environment environment: 環境設定
        :return RepositoryUtilStorage: ストレージユーティリティインスタンス
        """
        return cls(
            path=environment.storage_directory,
        )

    def search_image(self, path: RepositoryUtilStoragePathBase) -> DomainImage:
        """
        指定した論理パスに該当する画像を 1 件読み込み、ドメイン画像として返す。

        ファイル名に jpg / jpeg / png を付けたもののうち存在するものを探す。1 種類だけ存在する場合にそのファイルを開いて返す。
        0 件の場合は NotFoundError、複数拡張子が存在する場合は ConflictError。
        読み込みに失敗した場合（ファイルなし・権限・形式不正・圧縮爆弾・その他 I/O エラー）は NotFoundError または InternalServerError となる。

        :param RepositoryUtilStoragePathBase path: 画像の論理パス（ディレクトリ名とファイル名）
        :return DomainImage: 読み込んだ画像
        :raises NotFoundError: 該当ファイルが 1 件もない、または開けない場合
        :raises ConflictError: 同一ファイル名で複数拡張子のファイルが存在する場合
        :raises InternalServerError: アクセス・形式・圧縮爆弾・その他 I/O エラーの場合
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
        画像を指定した論理パスに 1 ファイルとして保存する。

        保存先の拡張子は画像のフォーマットに従う。既存ファイルは上書きする。
        保存に失敗した場合（PIL のエラーや I/O エラー）は InternalServerError となる。

        :param DomainImage image: 保存するドメイン画像
        :param RepositoryUtilStoragePathBase path: 保存先の論理パス（拡張子は画像フォーマット）
        :raises InternalServerError: 保存に失敗した場合
        """
        try:
            image.image.save(self.path / path.directory /
                             f"{path.name}.{image.format}")
        except ValueError as error:
            raise InternalServerError("画像を保存できません") from error
        except OSError as error:
            raise InternalServerError("画像を保存できません") from error
