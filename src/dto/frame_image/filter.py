from dataclasses import dataclass
from datetime import datetime

@dataclass
class DtoFrameImageFilter:
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
