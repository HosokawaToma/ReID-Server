from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results, Boxes
from domain.yolo.bounding_box import DomainYoloBoundingBox
from PIL import Image


class DomainYoloDetectionModel:
    PERSON_CLASS_ID: int = 0
    CLASSES: list[int] = [PERSON_CLASS_ID]
    IOU_THRESHOLD: float = 0.3
    CONFIDENCE_THRESHOLD: float = 0.25

    def __init__(self):
        self.model = YOLO("./resources/models/yolo11x.pt")

    def extract(self, image: Image.Image) -> list[DomainYoloBoundingBox]:
        results = self.model(
            image,
            classes=self.CLASSES,
            iou=self.IOU_THRESHOLD,
            conf=self.CONFIDENCE_THRESHOLD,
            verbose=False,
        )
        items: Results = results[0]
        if items.boxes is None:
            return []
        detections = []
        for box in items.boxes:
            box: Boxes
            xyxy = box.xyxy[0].cpu().numpy()
            xyxyn = box.xyxyn[0].cpu().numpy()
            xywhn = box.xywhn[0].cpu().numpy()
            detections.append(DomainYoloBoundingBox(
                class_id=int(box.cls[0].cpu().numpy()),
                confidence=float(box.conf[0].cpu().numpy()),
                x1=float(xyxy[0]),
                y1=float(xyxy[1]),
                x2=float(xyxy[2]),
                y2=float(xyxy[3]),
                original_x1=int(xyxyn[0]),
                original_y1=int(xyxyn[1]),
                original_x2=int(xyxyn[2]),
                original_y2=int(xyxyn[3]),
                original_width=int(xywhn[2]),
                original_height=int(xywhn[3]),
            ))
        return detections
