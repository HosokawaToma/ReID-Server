from dataclasses import dataclass
from datetime import datetime

@dataclass
class EntityPersonFlow:
    source_camera_id: int
    target_camera_id: int
    source_timestamp: datetime
    target_timestamp: datetime
