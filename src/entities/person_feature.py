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

    def __post_init__(self):
        if self.feature.ndim != 1:
            raise ValueError("Person feature must be a 1D tensor")
        if self.feature.shape[0] != 1280:
            raise ValueError("Person feature must be a 1280D tensor")

    def to_database_model(self):
        return DatabasePostgreSQLModelPersonFeature(
            feature=self.feature.tolist(),
            camera_id=self.camera_id,
            view_id=self.view_id,
            timestamp=self.timestamp,
        )
