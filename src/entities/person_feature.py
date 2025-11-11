from dataclasses import dataclass, field
import uuid
import torch
from datetime import datetime
from database.models.person_feature import DatabaseModelPersonFeature

@dataclass
class EntityPersonFeature:
    id: uuid.UUID | None
    person_id: uuid.UUID | None
    feature: torch.Tensor
    camera_id: int
    view_id: int
    timestamp: datetime

    def __post_init__(self):
        if self.id is None:
            self.id = uuid.uuid4()
        if self.person_id is None:
            self.person_id = uuid.uuid4()
        if self.feature.ndim != 1:
            raise ValueError("Person feature must be a 1D tensor")
        if self.feature.shape[0] != 1280:
            raise ValueError("Person feature must be a 1280D tensor")

    def to_database_model(self):
        return DatabaseModelPersonFeature(
            id=self.id,
            person_id=self.person_id,
            feature=self.feature.tolist(),
            camera_id=self.camera_id,
            view_id=self.view_id,
            timestamp=self.timestamp,
        )

    @staticmethod
    def from_database_model(model: DatabaseModelPersonFeature) -> "EntityPersonFeature":
        return EntityPersonFeature(
            id=uuid.UUID(str(model.id)),
            person_id=uuid.UUID(str(model.person_id)),
            feature=torch.tensor(model.feature),
            camera_id=int(str(model.camera_id)),
            view_id=int(str(model.view_id)),
            timestamp=datetime.fromisoformat(str(model.timestamp)),
        )
