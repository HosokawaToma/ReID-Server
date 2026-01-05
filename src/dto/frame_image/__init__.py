from dataclasses import dataclass
from datetime import datetime
import uuid
from PIL import Image

@dataclass
class DtoFrameImage:
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    image: Image.Image
