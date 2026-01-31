from error import InternalServerError
from redis import Redis, RedisError
from environment import Environment
import json
from typing import Awaitable
from enum import Enum

class RepositoryUtilRedisKey(str, Enum):
    PERSON_SNAPSHOT_CREATE = "person_snapshot:create"
    PERSON_SNAPSHOT_REID = "person_snapshot:reid"
    PERSON_SNAPSHOT_FEATURE_EXTRACT = "person_snapshot:feature_extract"


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
            raise InternalServerError("キューにデータを追加することに失敗しました") from error
        if result is None:
            raise InternalServerError("キューにデータを追加することに失敗しました")
        if isinstance(result, Awaitable):
            raise InternalServerError("キューにデータを追加することに失敗しました")

    def dequeue(self, key: RepositoryUtilRedisKey) -> dict[str, str]:
        """
        キューからデータを取得します
        常にデータにアクセスをかけることを想定しているため，タイムアウトを設けない
        """
        try:
            result = self.redis.blpop([key.value])
        except RedisError as error:
            raise InternalServerError("キューからデータを取得することに失敗しました") from error
        if result is None:
            raise InternalServerError("キューからデータを取得することに失敗しました")
        if isinstance(result, Awaitable):
            raise InternalServerError("キューからデータを取得することに失敗しました")
        if len(result) != 2:
            raise InternalServerError("キューからデータを取得することに失敗しました")
        value = result[1]
        if isinstance(value, str):
            pass
        elif isinstance(value, bytes):
            value = value.decode("utf-8")
        else:
            raise InternalServerError("キューからデータを取得することに失敗しました")
        data = json.loads(value)
        if not isinstance(data, dict):
            raise InternalServerError("キューからデータを取得することに失敗しました")
        return data
