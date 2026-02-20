from typing import ClassVar
from ultralytics.models.yolo import YOLO
from ultralytics.engine.results import Results
from PIL import Image

class ModuleYoloPoseEstimator:
    WEIGHTS_PATH: ClassVar[str] = "./resources/models/yolo11x-pose.pt"
    DEVICE: ClassVar[str] = "cuda"

    def __init__(self):
        self.model = YOLO(self.WEIGHTS_PATH)

    def extract(self, image: Image.Image) -> Results:
        results = self.model(image, device=self.DEVICE, verbose=False)
        items: Results = results[0]
        return items
