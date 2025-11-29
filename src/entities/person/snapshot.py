from dataclasses import dataclass, field
import uuid
import torch
from datetime import datetime
from PIL.Image import Image


@dataclass
class PersonSnapshotImage:
    image: Image
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class PersonSnapshot:
    image_id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    feature: torch.Tensor | None = None
