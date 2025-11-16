from dataclasses import dataclass
from datetime import datetime

@dataclass
class EntityApplicationIdentifyPersonSearchConditions:
    after: datetime
    before: datetime
    view_ids: list[int]
    camera_ids: list[int]
