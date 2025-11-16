from dataclasses import dataclass, field
import uuid
from datetime import datetime
from pathlib import Path
from database.models.person_image_path import DatabaseModelPersonImagePath

@dataclass
class EntityPersonImagePath:
    PATH_FORMAT = "{camera_id}/{view_id}/{timestamp}_{id}.jpg"
    image_id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    path: Path = field(init=False)

    def __post_init__(self):
        self.path = Path(self.PATH_FORMAT.format(
            camera_id=self.camera_id,
            view_id=self.view_id,
            timestamp=self.timestamp.strftime("%Y%m%d%H%M%S"),
            id=self.image_id,
        ))

    def to_database_model(self) -> DatabaseModelPersonImagePath:
        return DatabaseModelPersonImagePath(
            image_id=self.image_id,
            camera_id=self.camera_id,
            view_id=self.view_id,
            timestamp=self.timestamp,
            path=str(self.path),
        )

    @classmethod
    def from_database_model(cls, model: DatabaseModelPersonImagePath) -> "EntityPersonImagePath":
        return cls(
            image_id=uuid.UUID(str(model.image_id)),
            camera_id=int(str(model.camera_id)),
            view_id=int(str(model.view_id)),
            timestamp=datetime.fromisoformat(str(model.timestamp)),
        )

    @classmethod
    def from_path(cls, path: Path) -> "EntityPersonImagePath":
        if not path.is_file():
            raise ValueError("Path is not a file")
        if path.suffix != ".jpg":
            raise ValueError("Path is not a jpg file")
        try:
            image_id = path.stem.split("_")[1]
            camera_id = path.parent.name
            view_id = path.parent.parent.name
            timestamp = datetime.strptime(path.stem.split("_")[0], "%Y%m%d%H%M%S")
        except Exception as e:
            raise ValueError(f"Error parsing path: {e}")
        return cls(
            image_id=uuid.UUID(image_id),
            camera_id=int(camera_id),
            view_id=int(view_id),
            timestamp=timestamp,
        )
