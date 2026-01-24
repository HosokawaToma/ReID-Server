from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from environment import Environment
from error import InternalServerError
from typing import Type
from types import TracebackType


class RepositoryUtilDatabase:
    ENGINE_URL_TEMPLATE = "postgresql://{user}:{password}@{host}:{port}/{database}"
    _engine: Engine | None = None

    def __init__(self, host: str, port: str, database: str, user: str, password: str):
        if RepositoryUtilDatabase._engine is None:
            RepositoryUtilDatabase._engine = create_engine(
                self.ENGINE_URL_TEMPLATE.format(
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                    database=database
                )
            )
        self._session_maker = sessionmaker[Session](
            bind=RepositoryUtilDatabase._engine)
        self._session: Session | None = None

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryUtilDatabase":
        return cls(
            host=environment.database_host,
            port=environment.database_port,
            database=environment.database_database,
            user=environment.database_user,
            password=environment.database_password,
        )

    def __enter__(self) -> Session:
        """
        データベースのセッションを開く。
        :return Session: セッション
        :raise DatabaseOpenError: セッションを開くことに失敗した場合
        """
        if self._session is not None:
            raise InternalServerError("セッションがすでに開かれています")
        try:
            self._session = self._session_maker()
            self._session.begin()
            return self._session
        except SQLAlchemyError as error:
            if self._session:
                self._session.close()
                self._session = None
            raise InternalServerError("セッションを開くことに失敗しました") from error

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None
        ) -> None:
        """
        データベースのセッションを閉じる。
        例外が発生した場合はロールバックを行う。
        例外が発生しなかった場合はコミットを行う。
        :param Type[BaseException] | None exc_type: 例外の型
        :param BaseException | None exc_value: 例外の値
        :param TracebackType | None traceback: トレースバック
        :raise RepositoryUtilDatabaseCloseError: セッションが開かれていない場合
        :raise RepositoryUtilDatabaseCommitError: コミットに失敗した場合
        """
        if self._session is None:
            raise InternalServerError("セッションが開かれていません")
        try:
            if exc_type is not None:
                self._session.rollback()
                if exc_value is not None:
                   raise
                else:
                    raise exc_type()
            self._session.commit()
        except SQLAlchemyError as error:
            self._session.rollback()
            raise InternalServerError("セッションをコミットすることに失敗しました") from error
        finally:
            self._session.close()
            self._session = None
