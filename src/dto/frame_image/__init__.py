from dataclasses import dataclass
from datetime import datetime

@dataclass
class DtoFrameImage:
    camera_id: int
    view_id: int
    timestamp_after: datetime
    timestamp_before: datetime
