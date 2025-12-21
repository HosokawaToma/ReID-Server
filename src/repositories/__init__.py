from pathlib import Path
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from PIL import Image
import PIL
from dataclasses import dataclass
from typing import Type, Awaitable
from types import TracebackType
import glob
import io
from redis import Redis, RedisError
import json
import os
import concurrent.futures
from environment import Environment
from error import Error


class RepositoryDatabaseError(Error):
    pass

class RepositoryDatabaseOpenError(RepositoryDatabaseError):
    pass

class RepositoryDatabaseCommitError(RepositoryDatabaseError):
    pass

class RepositoryDatabaseCloseError(RepositoryDatabaseError):
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
            raise RepositoryDatabaseOpenError()
        try:
            self._session = self._session_maker()
            self._session.begin()
            return self._session
        except SQLAlchemyError as error:
            if self._session:
                self._session.close()
                self._session = None
            raise RepositoryDatabaseOpenError(error) from error

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> None:
        if self._session is None:
            raise RepositoryDatabaseOpenError()
        try:
            if exc_type is not None:
                self._session.rollback()
            else:
                self._session.commit()
        except SQLAlchemyError as error:
            self._session.rollback()
            raise RepositoryDatabaseCommitError(error) from error
        finally:
            self._session.close()
            self._session = None

@dataclass
class RepositoryStorageImage:
    name: str
    image: Image.Image


@dataclass
class RepositoryStorageImageName:
    name: str

class RepositoryStorageImageError(Error):
    pass

class RepositoryStorageImageNotFoundError(RepositoryStorageImageError):
    pass


class RepositoryStorageImageMultipleError(RepositoryStorageImageError):
    pass


class RepositoryStorageImageInvalidFormatError(RepositoryStorageImageError):
    pass


class RepositoryStorageImageInvalidSaveError(RepositoryStorageImageError):
    pass


class RepositoryStorageImageInvalidDeleteError(RepositoryStorageImageError):
    pass


class RepositoryStorageImagePermissionError(RepositoryStorageImageError):
    pass


class RepositoryStorageImageIsADirectoryError(RepositoryStorageImageError):
    pass

class RepositoryStorageImageUnidentifiedImageError(RepositoryStorageImageError):
    pass


class RepositoryStorageImageDecompressionBombError(RepositoryStorageImageError):
    pass

class RepositoryStorageImageOSError(RepositoryStorageImageError):
    pass

class RepositoryStorageImageCPUCountNoneError(RepositoryStorageImageError):
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
            raise RepositoryStorageImageNotFoundError()
        if len(image_names) > 1:
            raise RepositoryStorageImageMultipleError()
        image_name = image_names[0]
        return image_name

    def image_save(self, image: RepositoryStorageImage) -> None:
        try:
            if image.image.format is None:
                raise RepositoryStorageImageInvalidFormatError()
            image.image.save(self.images_directory /f"{image.name}.{image.image.format.lower()}")
        except ValueError as error:
            raise RepositoryStorageImageInvalidSaveError(error) from error
        except OSError as error:
            raise RepositoryStorageImageInvalidSaveError(error) from error

    def image_find_one(self, params: RepositoryStorageImageName) -> RepositoryStorageImage:
        try:
            image_name = self._fetch_image_name(params.name)
            with open(image_name, "rb") as file:
                file_content = file.read()
                image_stream = io.BytesIO(file_content)
                return RepositoryStorageImage(
                    name=params.name,
                    image=Image.open(image_stream).copy(),
                )
        except FileNotFoundError as error:
            raise RepositoryStorageImageNotFoundError(error) from error
        except PermissionError as error:
            raise RepositoryStorageImagePermissionError(error) from error
        except IsADirectoryError as error:
            raise RepositoryStorageImageIsADirectoryError(error) from error
        except PIL.UnidentifiedImageError as error:
            raise RepositoryStorageImageUnidentifiedImageError(error) from error
        except Image.DecompressionBombError as error:
            raise RepositoryStorageImageDecompressionBombError(error) from error
        except OSError as error:
            raise RepositoryStorageImageOSError(error) from error

    def image_find_all(self, params: list[RepositoryStorageImageName]) -> list[RepositoryStorageImage]:
        if len(params) == 0:
            return []
        cpu_count = os.cpu_count()
        if cpu_count is None:
            raise RepositoryStorageImageCPUCountNoneError()
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(params), cpu_count * 5)) as executor:
            future_to_index: dict[concurrent.futures.Future, int] = {
                executor.submit(self.image_find_one, param): index
                for index, param in enumerate(params)
            }
            results: list[RepositoryStorageImage | None] = [None] * len(params)
            exceptions: list[BaseException] = []
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    results[index] = future.result()
                except Exception as exc:
                    exceptions.append(exc)
            if exceptions:
                raise exceptions[0]
            return [result for result in results if result is not None]

    def image_delete(self, params: RepositoryStorageImageName) -> None:
        try:
            image_name = self._fetch_image_name(params.name)
            os.remove(image_name)
        except FileNotFoundError as error:
            raise RepositoryStorageImageNotFoundError(error) from error

    def image_delete_all(self, params: list[RepositoryStorageImageName]) -> None:
        try:
            image_names = [self._fetch_image_name(param.name) for param in params]
            for image_name in image_names:
                os.remove(image_name)
        except FileNotFoundError as error:
            raise RepositoryStorageImageNotFoundError(error) from error

class RepositoryRedisError(Error):
    pass

class RepositoryRedisPushError(RepositoryRedisError):
    pass

class RepositoryRedisDequeueError(RepositoryRedisError):
    pass

class RepositoryRedisResultNoneError(RepositoryRedisError):
    pass

class RepositoryRedisResultAwaitableError(RepositoryRedisError):
    pass

class RepositoryRedisResultLengthNot2Error(RepositoryRedisError):
    pass

class RepositoryRedisResultValueNotStrOrBytesError(RepositoryRedisError):
    pass

class RepositoryRedisResultDataNotDictError(RepositoryRedisError):
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
        try:
            result = self.redis.rpush(key, json.dumps(value))
        except RedisError as error:
            raise RepositoryRedisPushError(error) from error
        if result is None:
            raise RepositoryRedisResultNoneError()
        if isinstance(result, Awaitable):
            raise RepositoryRedisResultAwaitableError()

    def dequeue(self, key: str) -> dict[str, str]:
        try:
            result = self.redis.blpop([key])
        except RedisError as error:
            raise RepositoryRedisDequeueError(error) from error
        if result is None:
            raise RepositoryRedisResultNoneError()
        if isinstance(result, Awaitable):
            raise RepositoryRedisResultAwaitableError()
        if len(result) != 2:
            raise RepositoryRedisResultLengthNot2Error()
        value = result[1]
        if isinstance(value, str):
            pass
        elif isinstance(value, bytes):
            value = value.decode("utf-8")
        else:
            raise RepositoryRedisResultValueNotStrOrBytesError()
        data = json.loads(value)
        if not isinstance(data, dict):
            raise RepositoryRedisResultDataNotDictError()
        return data
