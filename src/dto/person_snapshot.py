import uuid
from dataclasses import dataclass
from datetime import datetime
import torch

@dataclass(frozen=True)
class DtoPersonSnapshot:
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    is_junk: bool
    person_id: uuid.UUID | None
    feature: torch.Tensor | None
