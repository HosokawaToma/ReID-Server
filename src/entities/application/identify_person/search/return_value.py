from dataclasses import dataclass
from PIL import Image
import uuid
from datetime import datetime

@dataclass
class EntityApplicationIdentifyPersonSearchReturnValue:
    image_id: uuid.UUID
    person_id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime

    def to_dict(self) -> dict:
        return {
            "image_id": str(self.image_id),
            "person_id": str(self.person_id),
            "camera_id": self.camera_id,
            "view_id": self.view_id,
            "timestamp": self.timestamp.isoformat(),
        }
