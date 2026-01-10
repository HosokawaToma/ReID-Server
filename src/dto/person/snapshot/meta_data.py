from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class DtoPersonSnapshotMetaData:
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    is_junk: bool
    person_id: uuid.UUID | None
