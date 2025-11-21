from PIL import Image
from datetime import datetime
import uuid
from dataclasses import dataclass, field

@dataclass
class EntityPersonImage:
    image: Image.Image
    camera_id: int
    view_id: int
    timestamp: datetime = field(default_factory=datetime.now)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
