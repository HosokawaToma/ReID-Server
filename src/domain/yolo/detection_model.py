from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results, Boxes
from domain.yolo.bounding_box import DomainYoloBoundingBox
from PIL import Image


class DomainYoloDetectionModel:
    PERSON_CLASS_ID: int = 0
    CLASSES: list[int] = [PERSON_CLASS_ID]
    def __init__(self):
        self.model = YOLO("./resources/models/yolo11x.pt")

    def extract(self, image: Image.Image) -> list[DomainYoloBoundingBox]:
        results = self.model(image, classes=self.CLASSES, verbose=False)
        items: Results = results[0]
        if items.boxes is None:
            return []
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
        return detections
