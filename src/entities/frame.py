from dataclasses import dataclass, field
from PIL import Image
import uuid
from datetime import datetime

@dataclass
class EntityFrame:
    image: Image.Image
    camera_id: int
    view_id: int
    timestamp: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
