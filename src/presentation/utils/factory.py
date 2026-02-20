"""
プレゼンテーション用ファクトリ

アップロード画像のDTO変換と、環境変数に依存するアプリケーションの取得を提供する。
"""
from fastapi import UploadFile
from dto.image import DtoImage
from error import ValidationError
import pathlib
from typing import Type, TypeVar, Generic
from applications import ApplicationBase
from environment import Environment
from fastapi import Depends


class PresentationUtilFactoryFromImage:
    """
    アップロードされた画像ファイルを画像 DTO に変換するファクトリ。

    ファイル名の拡張子から画像フォーマットを決定する。FastAPI の Depends で利用する。
    """

    async def __call__(self, image: UploadFile) -> DtoImage:
        """
        アップロード画像を読み取り、DTOに変換する。

        :param UploadFile image: アップロードされた画像
        :return DtoImage: 画像DTO
        :raises ValidationError: ファイル名または拡張子が無効な場合
        """
        if image.filename is None:
            raise ValidationError("image filename is None")
        content = await image.read()
        format = pathlib.Path(image.filename).suffix[1:]
        if format == "":
            raise ValidationError("image format is empty")
        return DtoImage(bytes=content, format=format.lower())


T = TypeVar("T", bound=ApplicationBase)


def get_environment() -> Environment:
    """
    環境変数を取得する。FastAPI の Depends で利用する。

    :return Environment: 環境変数
    """
    return Environment()


class PresentationUtilApplicationFactory(Generic[T]):
    """
    環境変数からアプリケーションインスタンスを生成するファクトリ。FastAPI の Depends で利用する。
    """

    def __init__(self, app_type: Type[T]):
        """
        ファクトリを初期化する。

        :param Type[T] app_type: アプリケーションクラス
        """
        self.app_type = app_type

    def __call__(self, environment: Environment = Depends(get_environment)) -> T:
        """
        環境変数からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境変数
        :return T: アプリケーションインスタンス
        """
        return self.app_type.create(environment)


def get_application(app_type: Type[T]) -> T:
    """
    指定したアプリケーションクラス用の Depends を返す。

    :param Type[T] app_type: アプリケーションクラス
    :return T: Depends の戻り値（リクエスト時にアプリケーションインスタンスが注入される）
    """
    return Depends(PresentationUtilApplicationFactory(app_type))
