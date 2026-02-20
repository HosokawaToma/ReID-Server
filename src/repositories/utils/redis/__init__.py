"""
Redisユーティリティ

キュー用のRedis接続とキー定義を提供する。
"""
from error import InternalServerError
from redis import Redis, RedisError
from environment import Environment
import json
from typing import Awaitable
from enum import Enum


class RepositoryUtilRedisKey(str, Enum):
    """Redisキュー用のキー名。"""
    PERSON_SNAPSHOT_CREATE = "person_snapshot:create"
    PERSON_SNAPSHOT_REID = "person_snapshot:reid"
    PERSON_SNAPSHOT_FEATURE_EXTRACT = "person_snapshot:feature_extract"
    PERSON_SNAPSHOT_DETECT_JUNK = "person_snapshot:detect_junk"


class RepositoryUtilRedis:
    """
    Redis接続を扱うユーティリティクラス。

    キューへの push / blpop（dequeue）を提供する。
    """

    def __init__(self, host: str, port: int, db: int):
        """
        Redis接続を初期化する。

        :param str host: Redisホスト
        :param int port: ポート
        :param int db: DB番号
        """
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
        )

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryUtilRedis":
        """
        環境変数からRedisユーティリティインスタンスを生成する。

        :param Environment environment: 環境変数
        :return RepositoryUtilRedis: Redisユーティリティインスタンス
        """
        return cls(
            host=environment.redis_host,
            port=environment.redis_port,
            db=environment.redis_db,
        )

    def push(self, value: dict[str, str], key: RepositoryUtilRedisKey) -> None:
        """
        指定キーのキュー末尾にデータを1件追加する。

        :param dict[str, str] value: 追加するデータ（JSON化される）
        :param RepositoryUtilRedisKey key: キューキー
        :raises InternalServerError: 追加に失敗した場合
        """
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
        指定キーのキュー先頭からデータを1件取り出す（ブロッキング、タイムアウトなし）。

        :param RepositoryUtilRedisKey key: キューキー
        :return dict[str, str]: 取り出したデータ
        :raises InternalServerError: 取得に失敗した場合
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
