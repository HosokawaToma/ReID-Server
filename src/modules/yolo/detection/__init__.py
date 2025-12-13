from PIL import Image
from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results, Boxes
from entities.yolo.detection import EntityYoloDetection

class ModuleYoloDetection:
    def __init__(self):
        self.model = YOLO("./resources/models/yolo11x-detection.pt")

    def extract(self, image: Image.Image) -> list[EntityYoloDetection]:
        results = self.model(image, verbose=False)
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
            cls = int(box.cls[0].cpu().numpy())
            detections.append(EntityYoloDetection(
                class_id=cls,
                confidence=conf,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
            ))
        return detections

