from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from environment import Environment
from error import Error
from typing import Type
from types import TracebackType

class DatabaseError(Error):
    pass

class DatabaseOpenError(DatabaseError):
    pass

class DatabaseCommitError(DatabaseError):
    pass

class DatabaseCloseError(DatabaseError):
    pass

class Database:
    ENGINE_URL_TEMPLATE = "postgresql://{user}:{password}@{host}:{port}/{database}"
    _engine: Engine | None = None

    def __init__(self, host: str, port: str, database: str, user: str, password: str):
        if Database._engine is None:
            Database._engine = create_engine(
                self.ENGINE_URL_TEMPLATE.format(
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                    database=database
                )
            )
        self._session_maker = sessionmaker[Session](
            bind=Database._engine)
        self._session: Session | None = None

    @classmethod
    def create(cls, environment: Environment) -> "Database":
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
            raise DatabaseOpenError()
        try:
            self._session = self._session_maker()
            self._session.begin()
            return self._session
        except SQLAlchemyError as error:
            if self._session:
                self._session.close()
                self._session = None
            raise DatabaseOpenError(error) from error

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
        :raise DatabaseCloseError: セッションが開かれていない場合
        :raise DatabaseCommitError: コミットに失敗した場合
        """
        if self._session is None:
            raise DatabaseCloseError()
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
            raise DatabaseCommitError(error) from error
        finally:
            self._session.close()
            self._session = None
