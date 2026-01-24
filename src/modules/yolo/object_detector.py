from typing import ClassVar
from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results
from PIL import Image

class ModuleYoloObjectDetector:
    WEIGHTS_PATH: ClassVar[str] = "./resources/models/yolo11x.pt"
    PERSON_CLASS: ClassVar[int] = 0
    IOU_THRESHOLD: ClassVar[float] = 0.5
    CONFIDENCE_THRESHOLD: ClassVar[float] = 0.5

    def __init__(self):
        self.model = YOLO(self.WEIGHTS_PATH)

    def extract_person(self, image: Image.Image) -> Results:
        results = self.model(
            image,
            classes=[self.PERSON_CLASS],
            iou=self.IOU_THRESHOLD,
            conf=self.CONFIDENCE_THRESHOLD,
            verbose=False,
        )
        items: Results = results[0]
        return items
