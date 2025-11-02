from dataclasses import dataclass, field
import uuid
import torch
from datetime import datetime

@dataclass
class EntityPersonFeature:
    feature: torch.Tensor
    camera_id: int
    view_id: int
    timestamp: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
