from database import Database
from entities.person_feature import EntityPersonFeature
from database.models.person_feature import DatabaseModelPersonFeature
import torch
from datetime import datetime
from typing import List
import uuid
from errors.modules.database import ErrorModuleDatabase
from entities.database.where.person_features import EntityDatabaseWherePersonFeatures
class ModuleDatabasePersonFeatures:
    NAME = "person_features"
    CAMERA_ID_KEY_OF_METADATA = "camera_id"
    VIEW_ID_KEY_OF_METADATA = "view_id"
    TIMESTAMP_KEY_OF_METADATA = "timestamp"

    def __init__(
        self,
        database: Database
        ):
        self.database = database

    def insert(self, person_feature: EntityPersonFeature) -> None:
        try:
            with self.database as db_session:
                db_session.add(person_feature.to_database_model())
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to insert person feature: {e}")

    def select_all(self) -> List[EntityPersonFeature]:
        try:
            with self.database as db_session:
                models = db_session.query(DatabaseModelPersonFeature).all()
                return [EntityPersonFeature.from_database_model(model) for model in models]
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to select all person features: {e}")

    def select_by_id(self, id: uuid.UUID) -> EntityPersonFeature:
        try:
            with self.database as db_session:
                model = db_session.query(DatabaseModelPersonFeature).filter(DatabaseModelPersonFeature.id == id).first()
                if model is None:
                    raise ErrorModuleDatabase(f"Person feature with id {id} not found")
                return EntityPersonFeature.from_database_model(model)
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to select person feature by id: {e}")

    def select_by_image_id(self, image_id: uuid.UUID) -> EntityPersonFeature:
        try:
            with self.database as db_session:
                model = db_session.query(DatabaseModelPersonFeature).filter(DatabaseModelPersonFeature.image_id == image_id).first()
                if model is None:
                    raise ErrorModuleDatabase(f"Person feature with image id {image_id} not found")
                return EntityPersonFeature.from_database_model(model)
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to select person feature by image id: {e}")

    def select_top_one_by_before_timestamp(self, feature: torch.Tensor, timestamp: datetime) -> EntityPersonFeature | None:
        try:
            with self.database as db_session:
                model = db_session.query(DatabaseModelPersonFeature) \
                    .filter(DatabaseModelPersonFeature.timestamp < timestamp) \
                    .order_by(DatabaseModelPersonFeature.feature.op("<=>")(feature.cpu().numpy().tolist())) \
                    .first()
                if model is None:
                    return None
                return EntityPersonFeature.from_database_model(model)
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to select top one person feature by before timestamp: {e}")

    def select_by_timestamp_range(self, after_timestamp: datetime | None, before_timestamp: datetime | None) -> List[EntityPersonFeature]:
        try:
            with self.database as db_session:
                query = db_session.query(DatabaseModelPersonFeature)
                if after_timestamp is not None:
                    query = query.filter(DatabaseModelPersonFeature.timestamp > after_timestamp)
                if before_timestamp is not None:
                    query = query.filter(DatabaseModelPersonFeature.timestamp < before_timestamp)
                return [EntityPersonFeature.from_database_model(model) for model in query.all()]
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to select person features by timestamp range: {e}")

    def update(self, person_feature: EntityPersonFeature) -> None:
        try:
            with self.database as db_session:
                db_session.merge(person_feature.to_database_model())
                db_session.commit()
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to update person feature: {e}")

    def delete_by_image_id(self, image_id: uuid.UUID) -> None:
        try:
            with self.database as db_session:
                db_session.query(DatabaseModelPersonFeature) \
                    .filter(DatabaseModelPersonFeature.image_id == image_id) \
                    .delete()
                db_session.commit()
        except Exception as e:
            raise ErrorModuleDatabase(f"Failed to delete person feature by image id: {e}")
