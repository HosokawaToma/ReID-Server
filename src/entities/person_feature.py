from dataclasses import dataclass, field
import uuid
import torch
from datetime import datetime
from repositories.database.person_features import RepositoryDatabasePersonFeatureModel

@dataclass
class EntityPersonFeature:
    feature: torch.Tensor
    camera_id: int
    view_id: int
    timestamp: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    image_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        if self.feature.ndim != 1:
            raise ValueError("Person feature must be a 1D tensor")
        if self.feature.shape[0] != 1280:
            raise ValueError("Person feature must be a 1280D tensor")
