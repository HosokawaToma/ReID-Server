from typing import ClassVar
from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results
from PIL import Image

class ModuleYoloInstanceSegmenter:
    WEIGHTS_PATH: ClassVar[str] = "./resources/models/yolo11x-seg.pt"
    PERSON_CLASS: ClassVar[int] = 0

    def __init__(self):
        self.model = YOLO(self.WEIGHTS_PATH)

    def extract(self, image: Image.Image) -> Results:
        results = self.model(
            image,
            classes=[self.PERSON_CLASS],
            verbose=False
        )
        return results[0]
