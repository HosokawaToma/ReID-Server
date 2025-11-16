from datetime import datetime
from entities.person_image_path import EntityPersonImagePath

class EntityCollectionPersonImagePaths:
    def __init__(self, items: list[EntityPersonImagePath]):
        self.items = items

    def filter(
        self,
        after_timestamp: datetime | None,
        before_timestamp: datetime | None,
        camera_ids: list[int] | None,
        view_ids: list[int] | None,
    ) -> "EntityCollectionPersonImagePaths":
        if after_timestamp is not None:
            self.items = [path for path in self.items if path.timestamp >= after_timestamp]
        if before_timestamp is not None:
            self.items = [path for path in self.items if path.timestamp <= before_timestamp]
        if camera_ids is not None:
            self.items = [path for path in self.items if path.camera_id in camera_ids]
        if view_ids is not None:
            self.items = [path for path in self.items if path.view_id in view_ids]
        return self
