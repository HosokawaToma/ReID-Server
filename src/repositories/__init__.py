from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from PIL import Image
from dataclasses import dataclass
from typing import Type
from types import TracebackType
import glob
import io

from environment import Environment

class RepositoryDatabaseError(Exception):
    pass

class RepositoryDatabase:
    ENGINE_URL_TEMPLATE = "postgresql://{user}:{password}@{host}:{port}/{database}"
    _engine: Engine | None = None

    def __init__(self, environment: Environment):
        if RepositoryDatabase._engine is None:
            RepositoryDatabase._engine = create_engine(
                self.ENGINE_URL_TEMPLATE.format(
                    user=environment.database_user,
                    password=environment.database_password,
                    host=environment.database_host,
                    port=environment.database_port,
                    database=environment.database_database
                )
            )
        self._session_maker = sessionmaker[Session](
            bind=RepositoryDatabase._engine)
        self._session: Session | None = None

    def __enter__(self) -> Session:
        if self._session is not None:
            raise RepositoryDatabaseError("Session is already open")
        try:
            self._session = self._session_maker()
            self._session.begin()
            return self._session
        except SQLAlchemyError as e:
            if self._session:
                self._session.close()
                self._session = None
            raise e

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> None:
        if self._session is None:
            raise RepositoryDatabaseError("Session is not open")
        try:
            if exc_type is not None:
                self._session.rollback()
            self._session.commit()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e
        finally:
            self._session.close()
            self._session = None

@dataclass
class RepositoryStorageImage:
    name: str
    image: Image.Image

class RepositoryStorageImageError(Exception):
    pass

@dataclass
class RepositoryStorageImageFindOneParams:
    name: str

@dataclass
class RepositoryStorageImageFindOneResult:
    name: str
    image: Image.Image

class StorageImageNotFoundError(RepositoryStorageImageError):
    pass

class StorageImageMultipleError(RepositoryStorageImageError):
    pass

class StorageImageInvalidError(RepositoryStorageImageError):
    pass

class RepositoryStorage:
    def __init__(self, environment: Environment):
        self.storage_directory = environment.storage_directory
        self.images_directory = self.storage_directory / "images"
        self.images_directory.mkdir(exist_ok=True)
        self.images_directory.mkdir(parents=True, exist_ok=True)

    def image_save(self, image: RepositoryStorageImage) -> None:
        if image.image.format == "JPEG":
            extension = "jpg"
        else:
            raise StorageImageInvalidError
        image.image.save(self.images_directory / f"{image.name}.{extension}")

    def image_find_one(self, params: RepositoryStorageImageFindOneParams) -> RepositoryStorageImageFindOneResult:
        image_names = glob.glob(str(self.images_directory / f"{params.name}.*"))
        if len(image_names) == 0:
            raise StorageImageNotFoundError
        if len(image_names) > 1:
            raise StorageImageMultipleError
        image_name = image_names[0]
        try:
            with open(image_name, "rb") as file:
                file_content = file.read()
                image_stream = io.BytesIO(file_content)
                return RepositoryStorageImageFindOneResult(
                    name=params.name,
                    image=Image.open(image_stream),
                )
        except FileNotFoundError:
            raise StorageImageNotFoundError
