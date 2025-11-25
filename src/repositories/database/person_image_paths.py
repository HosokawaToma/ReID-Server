from datetime import datetime
import uuid

from entities.person_image_path import EntityPersonImagePath
from repositories.database import RepositoryDatabaseEngine

from sqlalchemy.orm import Query
from dataclasses import dataclass

from migration.models.person_image_paths import MigrationModelPersonImagePath

class RepositoryDatabasePersonImagePathModel(MigrationModelPersonImagePath):
    def to_entity(self) -> EntityPersonImagePath:
        return EntityPersonImagePath(
            image_id=uuid.UUID(str(self.image_id)),
            camera_id=int(str(self.camera_id)),
            view_id=int(str(self.view_id)),
            timestamp=datetime.fromisoformat(str(self.timestamp)),
        )

    @staticmethod
    def from_entity(entity: EntityPersonImagePath) -> "RepositoryDatabasePersonImagePathModel":
        return RepositoryDatabasePersonImagePathModel(
            image_id=entity.image_id,
            camera_id=entity.camera_id,
            view_id=entity.view_id,
            timestamp=entity.timestamp,
            path=str(entity.path),
        )

    def to_dict(self) -> dict:
        return {
            "image_id": self.image_id,
            "camera_id": self.camera_id,
            "view_id": self.view_id,
            "timestamp": self.timestamp,
            "path": self.path,
        }

@dataclass
class RepositoryDatabasePersonImagePathsFilters:
    image_ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

    def filter(self, query: Query) -> Query:
        if self.image_ids is not None:
            query = query.filter(RepositoryDatabasePersonImagePathModel.image_id.in_(self.image_ids))
        if self.camera_ids is not None:
            query = query.filter(RepositoryDatabasePersonImagePathModel.camera_id.in_(self.camera_ids))
        if self.view_ids is not None:
            query = query.filter(RepositoryDatabasePersonImagePathModel.view_id.in_(self.view_ids))
        if self.timestamp_after is not None:
            query = query.filter(RepositoryDatabasePersonImagePathModel.timestamp >= self.timestamp_after)
        if self.timestamp_before is not None:
            query = query.filter(RepositoryDatabasePersonImagePathModel.timestamp <= self.timestamp_before)
        return query

class RepositoryDatabasePersonImagePathsError(Exception):
    pass

class RepositoryDatabasePersonImagePaths:
    def __init__(self, database: RepositoryDatabaseEngine):
        self.database = database

    def insert(self, person_image_path: EntityPersonImagePath) -> None:
        with self.database as db_session:
            db_session.add(RepositoryDatabasePersonImagePathModel.from_entity(person_image_path))

    def find_first(self, filters: RepositoryDatabasePersonImagePathsFilters | None = None) -> EntityPersonImagePath:
        with self.database as db_session:
            query = db_session.query(RepositoryDatabasePersonImagePathModel)
            if filters is not None:
                query = filters.filter(query)
            model = query.first()
            if model is None:
                raise RepositoryDatabasePersonImagePathsError("Person image path not found")
            return model.to_entity()

    def find_all(self, filters: RepositoryDatabasePersonImagePathsFilters | None = None) -> list[EntityPersonImagePath]:
        with self.database as db_session:
            query = db_session.query(RepositoryDatabasePersonImagePathModel)
            if filters is not None:
                query = filters.filter(query)
            return [model.to_entity() for model in query.all()]

    def merge(self, person_image_path: EntityPersonImagePath) -> None:
        with self.database as db_session:
            db_session.merge(RepositoryDatabasePersonImagePathModel.from_entity(person_image_path))

    def update(
        self,
        person_image_path: EntityPersonImagePath,
        filters: RepositoryDatabasePersonImagePathsFilters | None = None,
    ) -> None:
        with self.database as db_session:
            query = db_session.query(RepositoryDatabasePersonImagePathModel)
            if filters is not None:
                query = filters.filter(query)
            query.update(RepositoryDatabasePersonImagePathModel.from_entity(person_image_path).to_dict())
