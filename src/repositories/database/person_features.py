from repositories.database import RepositoryDatabaseEngine
from entities.person_feature import EntityPersonFeature
import torch
from datetime import datetime
from typing import List
import uuid
from migration.models.person_features import MigrationModelPersonFeature
from sqlalchemy.orm import Query
from dataclasses import dataclass

class RepositoryDatabasePersonFeatureModel(MigrationModelPersonFeature):

    def to_entity(self) -> EntityPersonFeature:
        return EntityPersonFeature(
            id=uuid.UUID(str(self.id)),
            image_id=uuid.UUID(str(self.image_id)),
            person_id=uuid.UUID(str(self.person_id)),
            feature=torch.tensor(self.feature),
            camera_id=int(str(self.camera_id)),
            view_id=int(str(self.view_id)),
            timestamp=datetime.fromisoformat(str(self.timestamp)),
        )

    @staticmethod
    def from_entity(entity: EntityPersonFeature) -> "RepositoryDatabasePersonFeatureModel":
        return RepositoryDatabasePersonFeatureModel(
            id=entity.id,
            image_id=entity.image_id,
            person_id=entity.person_id,
            feature=entity.feature.cpu(),
            camera_id=entity.camera_id,
            view_id=entity.view_id,
            timestamp=entity.timestamp,
        )

@dataclass
class RepositoryDatabasePersonFeaturesFilters:
    ids: list[uuid.UUID] | None = None
    image_ids: list[uuid.UUID] | None = None
    person_ids: list[uuid.UUID] | None = None
    feature: torch.Tensor | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

    def filter(self, query: Query) -> Query:
        if self.ids is not None:
            query = query.filter(RepositoryDatabasePersonFeatureModel.id.in_(self.ids))
        if self.image_ids is not None:
            query = query.filter(RepositoryDatabasePersonFeatureModel.image_id.in_(self.image_ids))
        if self.person_ids is not None:
            query = query.filter(RepositoryDatabasePersonFeatureModel.person_id.in_(self.person_ids))
        if self.feature is not None:
            query = query.filter(RepositoryDatabasePersonFeatureModel.feature == self.feature)
        if self.camera_ids is not None:
            query = query.filter(RepositoryDatabasePersonFeatureModel.camera_id.in_(self.camera_ids))
        if self.view_ids is not None:
            query = query.filter(RepositoryDatabasePersonFeatureModel.view_id.in_(self.view_ids))
        if self.timestamp_after is not None:
            query = query.filter(RepositoryDatabasePersonFeatureModel.timestamp >= self.timestamp_after)
        if self.timestamp_before is not None:
            query = query.filter(RepositoryDatabasePersonFeatureModel.timestamp <= self.timestamp_before)
        return query

@dataclass
class RepositoryDatabasePersonFeatureOrderings:
    timestamp_descending: bool | None = None
    timestamp_ascending: bool | None = None
    feature_to_nearest: torch.Tensor | None = None

    def order_by(self, query: Query) -> Query:
        if self.timestamp_descending is not None:
            query = query.order_by(RepositoryDatabasePersonFeatureModel.timestamp.desc())
        if self.timestamp_ascending is not None:
            query = query.order_by(RepositoryDatabasePersonFeatureModel.timestamp.asc())
        if self.feature_to_nearest is not None:
            query = query.order_by(RepositoryDatabasePersonFeatureModel.feature.op("<=>")(self.feature_to_nearest.cpu().numpy().tolist()))
        return query

class RepositoryDatabasePersonFeaturesError(Exception):
    pass

class RepositoryDatabasePersonFeatures:
    def __init__(
        self,
        database: RepositoryDatabaseEngine
    ):
        self.database = database

    def add(self, person_feature: EntityPersonFeature) -> None:
        with self.database as db_session:
            db_session.add(RepositoryDatabasePersonFeatureModel.from_entity(person_feature))

    def find_all(
        self,
        filters: RepositoryDatabasePersonFeaturesFilters | None = None,
        orderings: RepositoryDatabasePersonFeatureOrderings | None = None
    ) -> List[EntityPersonFeature]:
        with self.database as db_session:
            query = db_session.query(RepositoryDatabasePersonFeatureModel)
            if filters is not None:
                query = filters.filter(query)
            if orderings is not None:
                query = orderings.order_by(query)
            return [model.to_entity() for model in query.all()]

    def find_first(
        self,
        filters: RepositoryDatabasePersonFeaturesFilters | None = None,
        orderings: RepositoryDatabasePersonFeatureOrderings | None = None
    ) -> EntityPersonFeature:
        with self.database as db_session:
            query = db_session.query(RepositoryDatabasePersonFeatureModel)
            if filters is not None:
                query = filters.filter(query)
            if orderings is not None:
                query = orderings.order_by(query)
            model = query.first()
            if model is None:
                raise RepositoryDatabasePersonFeaturesError("Person feature not found")
            return model.to_entity()

    def merge(self, person_feature: EntityPersonFeature) -> None:
        with self.database as db_session:
            db_session.merge(RepositoryDatabasePersonFeatureModel.from_entity(person_feature))

    def delete(self, filters: RepositoryDatabasePersonFeaturesFilters | None = None) -> None:
        with self.database as db_session:
            query = db_session.query(RepositoryDatabasePersonFeatureModel)
            if filters is not None:
                query = filters.filter(query)
            query.delete()
