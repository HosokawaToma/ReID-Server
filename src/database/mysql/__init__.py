from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Type
from types import TracebackType

class DatabaseMySQL:
    ENGINE_URL_TEMPLATE = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    _engine: Engine | None = None

    def __new__(cls, host: str, port: str, database: str, user: str, password: str):
        if cls._engine is None:
            engine_url = cls.ENGINE_URL_TEMPLATE.format(user=user, password=password, host=host, port=port, database=database)
            cls._engine = create_engine(engine_url)
        return super().__new__(engine_url)

    def __init__(self):
        if self._engine is None:
            raise ValueError("Engine is not initialized")
        self._session_maker = sessionmaker[Session](bind=self._engine)
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
            self._session.close()
            self._session = None
