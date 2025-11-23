from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import Query, declarative_base
from datetime import datetime
from dataclasses import dataclass
from repositories.database import RepositoryDatabaseEngine
from entities.camera_client import EntityCameraClient

Base = declarative_base()

class RepositoryDatabaseCameraClientModel(Base):
    __tablename__ = "camera_clients"
    id = Column[str](String(255), primary_key=True)
    hashed_password = Column[str](String(255))
    camera_id = Column[int](Integer)
    view_id = Column[int](Integer)
    created_at = Column[datetime](DateTime, default=datetime.now)
    updated_at = Column[datetime](
        DateTime, default=datetime.now, onupdate=datetime.now)

    def to_entity(self) -> EntityCameraClient:
        return EntityCameraClient(
            id=str(self.id),
            hashed_password=str(self.hashed_password),
            camera_id=int(str(self.camera_id)),
            view_id=int(str(self.view_id)),
        )

    @staticmethod
    def from_entity(entity: EntityCameraClient) -> "RepositoryDatabaseCameraClientModel":
        return RepositoryDatabaseCameraClientModel(
            id=entity.id,
            hashed_password=entity.hashed_password,
            camera_id=entity.camera_id,
            view_id=entity.view_id,
        )


@dataclass
class RepositoryDatabaseCameraClientsFilters:
    id: str | None = None

    def filter(self, query: Query) -> Query:
        if self.id is not None:
            query = query.filter(
                RepositoryDatabaseCameraClientModel.id == self.id)
        return query

class RepositoryDatabaseCameraClientError(Exception):
    pass

class RepositoryDatabaseCameraClients:
    def __init__(self, database: RepositoryDatabaseEngine):
        self.database = database

    def add(self, camera_client: EntityCameraClient) -> None:
        with self.database as db_session:
            db_session.add(RepositoryDatabaseCameraClientModel.from_entity(camera_client))

    def find_first(self, filters: RepositoryDatabaseCameraClientsFilters | None = None) -> EntityCameraClient:
        with self.database as db_session:
            query = db_session.query(RepositoryDatabaseCameraClientModel)
            if filters is not None:
                query = filters.filter(query)
            model = query.first()
            if model is None:
                raise RepositoryDatabaseCameraClientError("Camera client not found")
            return model.to_entity()

    def merge(self, camera_client: EntityCameraClient) -> None:
        with self.database as db_session:
            db_session.merge(RepositoryDatabaseCameraClientModel.from_entity(camera_client))
