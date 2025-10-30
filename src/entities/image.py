from PIL import Image
from datetime import datetime
import uuid
from dataclasses import dataclass

@dataclass
class EntityImage:
    id: uuid.UUID | None
    image: Image.Image
    camera_id: int
    view_id: int
    timestamp: datetime

    def __post_init__(self):
        if self.id is None:
            self.id = uuid.uuid4()
