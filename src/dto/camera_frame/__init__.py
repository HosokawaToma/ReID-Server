from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class DtoCameraFrame:
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
