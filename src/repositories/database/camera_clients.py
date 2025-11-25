from migration.models.camera_clients import MigrationModelCameraClient
from sqlalchemy.orm import Query
from dataclasses import dataclass
from repositories.database import RepositoryDatabaseEngine
from entities.camera_client import EntityCameraClient

class RepositoryDatabaseCameraClientModel(MigrationModelCameraClient):
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
    ids: list[str] | None = None

    def filter(self, query: Query) -> Query:
        if self.ids is not None:
            query = query.filter(RepositoryDatabaseCameraClientModel.id.in_(self.ids))
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
