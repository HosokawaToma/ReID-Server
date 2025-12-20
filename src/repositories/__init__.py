from pathlib import Path
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from PIL import Image
from dataclasses import dataclass
from typing import Type, Awaitable, Any
from types import TracebackType
import glob
import io
from redis import Redis
import json
import os
from typing import Callable, Iterable
import concurrent.futures
from environment import Environment
from error import Error


class RepositoryDatabaseError(Error):
    pass


class RepositoryDatabase:
    ENGINE_URL_TEMPLATE = "postgresql://{user}:{password}@{host}:{port}/{database}"
    _engine: Engine | None = None

    def __init__(self, host: str, port: str, database: str, user: str, password: str):
        if RepositoryDatabase._engine is None:
            RepositoryDatabase._engine = create_engine(
                self.ENGINE_URL_TEMPLATE.format(
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                    database=database
                )
            )
        self._session_maker = sessionmaker[Session](
            bind=RepositoryDatabase._engine)
        self._session: Session | None = None

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryDatabase":
        return cls(
            host=environment.database_host,
            port=environment.database_port,
            database=environment.database_database,
            user=environment.database_user,
            password=environment.database_password,
        )

    def __enter__(self) -> Session:
        if self._session is not None:
            raise RepositoryDatabaseError("Session is already open")
        try:
            self._session = self._session_maker()
            self._session.begin()
            return self._session
        except SQLAlchemyError as error:
            if self._session:
                self._session.close()
                self._session = None
            raise error

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
            else:
                self._session.commit()
        except SQLAlchemyError as error:
            self._session.rollback()
            raise error
        finally:
            self._session.close()
            self._session = None

@dataclass
class RepositoryStorageImage:
    name: str
    image: Image.Image


@dataclass
class RepositoryStorageImageFindParams:
    name: str


@dataclass
class RepositoryStorageImageFindResult:
    name: str
    image: Image.Image


@dataclass
class RepositoryStorageImageDeleteParams:
    name: str


class RepositoryStorageImageError(Error):
    pass


class RepositoryStorageImageFindError(RepositoryStorageImageError):
    pass


class RepositoryStorageImageSaveError(RepositoryStorageImageError):
    pass


class RepositoryStorageImageDeleteError(RepositoryStorageImageError):
    pass


class RepositoryStorage:
    def __init__(self, path: Path, directory: str):
        self.storage_directory = path
        self.images_directory = self.storage_directory / directory
        self.images_directory.mkdir(exist_ok=True, parents=True)

    @classmethod
    def create(cls, environment: Environment, directory: str) -> "RepositoryStorage":
        return cls(
            path=environment.storage_directory,
            directory=directory,
        )

    def _fetch_image_name(self, name: str) -> str:
        image_names = glob.glob(
            str(self.images_directory / f"{name}.*"))
        if len(image_names) == 0:
            raise RepositoryStorageImageFindError(f"image not found: {name}")
        if len(image_names) > 1:
            raise RepositoryStorageImageFindError(f"image multiple: {name}")
        image_name = image_names[0]
        return image_name

    def image_save(self, image: RepositoryStorageImage) -> None:
        if image.image.format is None:
            raise RepositoryStorageImageSaveError(
                f"image format is None: {image.name}")
        image.image.save(self.images_directory /
                         f"{image.name}.{image.image.format.lower()}")

    def image_find_one(self, params: RepositoryStorageImageFindParams) -> RepositoryStorageImageFindResult:
        image_name = self._fetch_image_name(params.name)
        with open(image_name, "rb") as file:
            file_content = file.read()
            image_stream = io.BytesIO(file_content)
            return RepositoryStorageImageFindResult(
                name=params.name,
                image=Image.open(image_stream),
            )

    def image_find_all(self, params: list[RepositoryStorageImageFindParams]) -> list[RepositoryStorageImageFindResult]:
        if len(params) == 0:
            return []
        cpu_count = os.cpu_count()
        if cpu_count is None:
            raise RepositoryStorageImageFindError("cpu count is None")
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(params), cpu_count * 5)) as executor:
            futures = [executor.submit(self.image_find_one, param)
                       for param in params]
            results = [future.result() for future in futures]
            return results

    def image_delete(self, params: RepositoryStorageImageDeleteParams) -> None:
        image_name = self._fetch_image_name(params.name)
        os.remove(image_name)


class RepositoryRedisError(Error):
    pass


class RepositoryRedisPushError(RepositoryRedisError):
    pass


class RepositoryRedisDequeueError(RepositoryRedisError):
    pass


class RepositoryRedis:
    def __init__(self, host: str, port: int, db: int):
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
        )

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryRedis":
        return cls(
            host=environment.redis_host,
            port=environment.redis_port,
            db=environment.redis_db,
        )

    def push(self, value: dict[str, str], key: str) -> None:
        result = self.redis.rpush(key, json.dumps(value))
        if result is None:
            raise RepositoryRedisPushError("result is None")
        if isinstance(result, Awaitable):
            raise RepositoryRedisPushError("result is Awaitable")

    def dequeue(self, key: str) -> dict[str, str]:
        result = self.redis.blpop([key])
        if result is None:
            raise RepositoryRedisDequeueError("result is None")
        if isinstance(result, Awaitable):
            raise RepositoryRedisDequeueError("result is Awaitable")
        if len(result) != 2:
            raise RepositoryRedisDequeueError("result length is not 2")
        value = result[1]
        if isinstance(value, str):
            pass
        elif isinstance(value, bytes):
            value = value.decode("utf-8")
        else:
            raise RepositoryRedisDequeueError("value is not str or bytes")
        data = json.loads(value)
        if not isinstance(data, dict):
            raise RepositoryRedisDequeueError("data is not dict")
        return data
