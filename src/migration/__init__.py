"""
マイグレーション用データベース接続

SQLAlchemy エンジンとセッションを提供し、コンテキストマネージャでトランザクションを扱う。
"""
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Type
from types import TracebackType


class Database:
    """
    データベース接続を管理するクラス。

    エンジンはクラス変数でキャッシュし、コンテキストマネージャでセッションの開始・コミット/ロールバック・終了を行う。
    """
    ENGINE_URL_TEMPLATE = "postgresql://{user}:{password}@{host}:{port}/{database}"
    _engine: Engine | None = None

    def __init__(self, host: str, port: str, database: str, user: str, password: str) -> None:
        """
        接続情報で初期化する。未作成時はエンジンを作成し、セッションファクトリを用意する。

        :param str host: ホスト
        :param str port: ポート
        :param str database: データベース名
        :param str user: ユーザー名
        :param str password: パスワード
        """
        if Database._engine is None:
            engine_url = self.ENGINE_URL_TEMPLATE.format(
                user=user, password=password, host=host, port=port, database=database
            )
            Database._engine = create_engine(engine_url)

        self._session_maker = sessionmaker[Session](bind=Database._engine)
        self._session: Session | None = None

    def __enter__(self) -> Session:
        """
        セッションを開始し、トランザクションを開始する。

        :return Session: SQLAlchemy セッション
        :raises ValueError: 既にセッションが開いている場合
        :raises SQLAlchemyError: 接続失敗時
        """
        if self._session is not None:
            raise ValueError("Session is already open")
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
        """
        例外時はロールバック、正常時はコミットし、セッションを閉じる。

        :param Type[BaseException] | None exc_type: 例外型
        :param BaseException | None exc_value: 例外インスタンス
        :param TracebackType | None traceback: トレースバック
        """
        if self._session is None:
            raise ValueError("Session is not open")
        try:
            if exc_type is not None:
                self._session.rollback()
            else:
                self._session.commit()
        except SQLAlchemyError as e:
            self._session.close()
            self._session = None
            raise e
        finally:
            if self._session:
                self._session.close()
                self._session = None
