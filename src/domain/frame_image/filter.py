from dataclasses import dataclass
from datetime import datetime
from dto.frame_image.filter import DtoFrameImageFilter

@dataclass
class DomainFrameImageFilter:
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

    @classmethod
    def from_dto(cls, dto: DtoFrameImageFilter) -> "DomainFrameImageFilter":
        filter = cls()
        filter.camera_ids = dto.camera_ids
        filter.view_ids = dto.view_ids
        filter.timestamp_after = dto.timestamp_after
        filter.timestamp_before = dto.timestamp_before
        return filter
