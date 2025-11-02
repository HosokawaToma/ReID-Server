from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Type
from types import TracebackType


class DatabaseMySQL:
    ENGINE_URL_TEMPLATE = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    _engine: Engine | None = None

    def __init__(self, host: str, port: str, database: str, user: str, password: str):

        if DatabaseMySQL._engine is None:
            engine_url = self.ENGINE_URL_TEMPLATE.format(
                user=user, password=password, host=host, port=port, database=database
            )
            DatabaseMySQL._engine = create_engine(engine_url)

        self._session_maker = sessionmaker[Session](bind=DatabaseMySQL._engine)
        self._session: Session | None = None

    def __enter__(self) -> Session:
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
