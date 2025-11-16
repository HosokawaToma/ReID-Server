from dataclasses import dataclass
from PIL import Image
import uuid
from datetime import datetime

@dataclass
class EntityApplicationIdentifyPersonSearchReturnValue:
    image: Image.Image
    person_id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
