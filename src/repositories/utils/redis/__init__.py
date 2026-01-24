from error import Error
from redis import Redis, RedisError
from environment import Environment
import json
from typing import Awaitable
from enum import Enum

class RepositoryUtilRedisKey(str, Enum):
    PERSON_SNAPSHOT_CREATE = "person_snapshot:create"
    PERSON_SNAPSHOT_REID = "person_snapshot:reid"

class RepositoryUtilRedisError(Error):
    pass


class RepositoryUtilRedisPushError(RepositoryUtilRedisError):
    pass


class RepositoryUtilRedisDequeueError(RepositoryUtilRedisError):
    pass


class RepositoryUtilRedisResultNoneError(RepositoryUtilRedisError):
    pass


class RepositoryUtilRedisResultAwaitableError(RepositoryUtilRedisError):
    pass


class RepositoryUtilRedisResultLengthNot2Error(RepositoryUtilRedisError):
    pass


class RepositoryUtilRedisResultValueNotStrOrBytesError(RepositoryUtilRedisError):
    pass


class RepositoryUtilRedisResultDataNotDictError(RepositoryUtilRedisError):
    pass


class RepositoryUtilRedis:
    def __init__(self, host: str, port: int, db: int):
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
        )

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryUtilRedis":
        return cls(
            host=environment.redis_host,
            port=environment.redis_port,
            db=environment.redis_db,
        )

    def push(self, value: dict[str, str], key: RepositoryUtilRedisKey) -> None:
        try:
            result = self.redis.rpush(key.value, json.dumps(value))
        except RedisError as error:
            raise RepositoryUtilRedisPushError(error) from error
        if result is None:
            raise RepositoryUtilRedisResultNoneError()
        if isinstance(result, Awaitable):
            raise RepositoryUtilRedisResultAwaitableError()

    def dequeue(self, key: RepositoryUtilRedisKey) -> dict[str, str]:
        """
        キューからデータを取得します
        常にデータにアクセスをかけることを想定しているため，タイムアウトを設けない
        """
        try:
            result = self.redis.blpop([key.value])
        except RedisError as error:
            raise RepositoryUtilRedisDequeueError(error) from error
        if result is None:
            raise RepositoryUtilRedisResultNoneError()
        if isinstance(result, Awaitable):
            raise RepositoryUtilRedisResultAwaitableError()
        if len(result) != 2:
            raise RepositoryUtilRedisResultLengthNot2Error()
        value = result[1]
        if isinstance(value, str):
            pass
        elif isinstance(value, bytes):
            value = value.decode("utf-8")
        else:
            raise RepositoryUtilRedisResultValueNotStrOrBytesError()
        data = json.loads(value)
        if not isinstance(data, dict):
            raise RepositoryUtilRedisResultDataNotDictError()
        return data
