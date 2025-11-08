from dataclasses import dataclass, field
import uuid
import torch
from datetime import datetime
from database.postgresql.models.person_feature import DatabasePostgreSQLModelPersonFeature

@dataclass
class EntityPersonFeature:
    feature: torch.Tensor
    camera_id: int
    view_id: int
    timestamp: datetime

    def to_database_model(self):
        return DatabasePostgreSQLModelPersonFeature(
            feature=self.feature.tolist(),
            camera_id=self.camera_id,
            view_id=self.view_id,
            timestamp=self.timestamp,
        )
