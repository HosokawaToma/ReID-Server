from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class DomainPersonFlow:
    person_id: uuid.UUID
    source_camera_id: int
    target_camera_id: int
    source_timestamp: datetime
    target_timestamp: datetime
