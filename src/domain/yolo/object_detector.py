from dataclasses import dataclass
from ultralytics.engine.results import Results, Boxes
from domain.yolo.bounding_box import DomainYoloBoundingBox
from domain.yolo.bounding_box_sequence import DomainYoloBoundingBoxSequence
from domain.utils.base import DomainUtilsBase
from domain.image import DomainImage
from modules.yolo.object_detector import ModuleYoloObjectDetector

@dataclass(frozen=True)
class DomainYoloObjectDetector(DomainUtilsBase):
    """
    YOLOの物体検出器のドメインモデル
    """
    model: ModuleYoloObjectDetector

    def extract_person(self, image: DomainImage) -> DomainYoloBoundingBoxSequence:
        results = self.model.extract_person(
            image.image,
        )
        items: Results = results[0]
        if items.boxes is None:
            return DomainYoloBoundingBoxSequence(items=[])
        detections = []
        for box in items.boxes:
            box: Boxes
            xyxy = box.xyxy[0].cpu().numpy()
            x1 = float(xyxy[0])
            y1 = float(xyxy[1])
            x2 = float(xyxy[2])
            y2 = float(xyxy[3])
            conf = float(box.conf[0].cpu().numpy())
            class_id = int(box.cls[0].cpu().numpy())
            detections.append(DomainYoloBoundingBox(
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                confidence=conf,
                class_id=class_id,
            ))
        return DomainYoloBoundingBoxSequence(items=detections)
