from dataclasses import dataclass
import uuid
import torch
from datetime import datetime

@dataclass
class EntityPersonFeature:
    id: uuid.UUID | None
    feature: torch.Tensor
    camera_id: int
    view_id: int
    timestamp: datetime

    def __post_init__(self):
        if self.id is None:
            self.id = uuid.uuid4()
