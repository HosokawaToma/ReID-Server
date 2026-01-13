from PIL import Image
from datetime import datetime
from dataclasses import dataclass, field
import uuid

from domain.yolo.detection_model import DomainYoloDetectionModel
from domain.person.snapshot import DomainPersonSnapshot
from domain.person.snapshot.detection import DomainPersonSnapshotDetection

@dataclass
class DomainFrameImage:
    camera_id: int
    view_id: int
    timestamp: datetime
    image: Image.Image
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def detect_person(self, detection_model: DomainYoloDetectionModel) -> tuple[list[DomainPersonSnapshot], list[DomainPersonSnapshotDetection]]:
        detections = detection_model.extract(self.image)
        person_snapshots = [DomainPersonSnapshot(
            camera_id=self.camera_id,
            view_id=self.view_id,
            timestamp=self.timestamp,
            image=detection.crop(self.image),
        ) for detection in detections]
        person_snapshot_detections = [DomainPersonSnapshotDetection(
            person_snapshot_id=person_snapshot.id,
            class_id=detection.class_id,
            confidence=detection.confidence,
            x=detection.original_x1,
            y=detection.original_y1,
            width=detection.original_width,
            height=detection.original_height,
        ) for person_snapshot in person_snapshots for detection in detections]
        return person_snapshots, person_snapshot_detections
