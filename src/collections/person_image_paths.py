from dataclasses import dataclass
from datetime import datetime
from entities.person_image_path import EntityPersonImagePath

@dataclass
class CollectionPersonImagePathsFilter:
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None

class CollectionPersonImagePaths:
    def __init__(self, items: list[EntityPersonImagePath]):
        self.items = items

    def filter(
        self,
        filter: CollectionPersonImagePathsFilter,
    ) -> "CollectionPersonImagePaths":
        if filter.after_timestamp is not None:
            self.items = [path for path in self.items if path.timestamp >= filter.after_timestamp]
        if filter.before_timestamp is not None:
            self.items = [path for path in self.items if path.timestamp <= filter.before_timestamp]
        if filter.camera_ids is not None:
            self.items = [path for path in self.items if path.camera_id in filter.camera_ids]
        if filter.view_ids is not None:
            self.items = [path for path in self.items if path.view_id in filter.view_ids]
        return self
