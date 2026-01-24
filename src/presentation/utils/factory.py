from fastapi import UploadFile
from dto.image import DtoImage
from error import ValidationError
import pathlib
from typing import Type, TypeVar, Generic
from applications import ApplicationBase
from environment import Environment
from fastapi import Depends


class PresentationUtilFactoryFromImage:
    async def __call__(self, image: UploadFile) -> DtoImage:
        if image.filename is None:
            raise ValidationError("image filename is None")
        content = await image.read()
        format = pathlib.Path(image.filename).suffix[1:]
        if format == "":
            raise ValidationError("image format is empty")
        return DtoImage(bytes=content, format=format.lower())


T = TypeVar("T", bound=ApplicationBase)


def get_environment():
    return Environment()

class PresentationUtilApplicationFactory(Generic[T]):
    def __init__(self, app_type: Type[T]):
        self.app_type = app_type

    def __call__(self, environment: Environment = Depends(get_environment)) -> T:
        return self.app_type.create(environment)


def get_application(app_type: Type[T]) -> T:
    return Depends(PresentationUtilApplicationFactory(app_type))
