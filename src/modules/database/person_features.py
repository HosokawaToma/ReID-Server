from database import Database
from entities.person_feature import EntityPersonFeature
from database.models.person_feature import DatabaseModelPersonFeature
import torch
from datetime import datetime
from typing import List
import uuid
from errors.modules.database import ErrorModuleDatabase
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
        with self.database as db_session:
            db_session.add(person_feature.to_database_model())

    def select_all(self) -> List[EntityPersonFeature]:
        with self.database as db_session:
            models = db_session.query(DatabaseModelPersonFeature).all()
            return [EntityPersonFeature.from_database_model(model) for model in models]

    def select_by_id(self, id: uuid.UUID) -> EntityPersonFeature:
        with self.database as db_session:
            model = db_session.query(DatabaseModelPersonFeature).filter(DatabaseModelPersonFeature.id == id).first()
            if model is None:
                raise ErrorModuleDatabase(f"Person feature with id {id} not found")
            return EntityPersonFeature.from_database_model(model)

    def select_top_one_by_before_timestamp(self, feature: torch.Tensor, timestamp: datetime) -> EntityPersonFeature | None:
        with self.database as db_session:
            model = db_session.query(DatabaseModelPersonFeature) \
                .filter(DatabaseModelPersonFeature.timestamp < timestamp) \
                .order_by(DatabaseModelPersonFeature.feature.op("<=>")(feature.cpu().numpy().tolist())) \
                .first()
            if model is None:
                return None
            return EntityPersonFeature.from_database_model(model)

    def update(self, person_feature: EntityPersonFeature) -> None:
        with self.database as db_session:
            db_session.merge(person_feature.to_database_model())
            db_session.commit()
