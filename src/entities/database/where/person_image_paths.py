from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class EntityDatabaseWherePersonImagePath:
    after: datetime | None = None
    before: datetime | None = None
    view_ids: list[int] | None = None
    camera_ids: list[int] | None = None
    image_ids: list[uuid.UUID] | None = None
