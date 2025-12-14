from PIL import Image
from datetime import datetime
from dataclasses import dataclass, field
import uuid

from domain.yolo.detection_model import DomainYoloDetectionModel
from domain.person.snapshot import DomainPersonSnapshot

@dataclass
class DomainFrameImage:
    camera_id: int
    view_id: int
    timestamp: datetime
    image: Image.Image
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def crop_person(self, detection_model: DomainYoloDetectionModel) -> list[DomainPersonSnapshot]:
        detections = detection_model.extract(self.image)
        return [DomainPersonSnapshot(
            camera_id=self.camera_id,
            view_id=self.view_id,
            timestamp=self.timestamp,
            image=detection.crop(self.image),
        ) for detection in detections]
