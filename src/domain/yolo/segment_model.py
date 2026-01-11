from ultralytics.models.yolo import YOLO
from domain.yolo.mask import DomainYoloMask
from ultralytics.engine.results import Results
from PIL import Image

class DomainYoloSegmentModel:
    def __init__(self):
        self.model = YOLO("./resources/models/yolo11x-seg.pt")

    def _extract(self, image: Image.Image) -> list[DomainYoloMask]:
        results = self.model(image, classes=[0], verbose=False)
        items: Results = results[0]
        if items.masks is None:
            return []
        masks = []
        for mask in items.masks:
            masks.append(DomainYoloMask(mask.xy.pop()))
        return masks

    def is_one_person(self, image: Image.Image) -> bool:
        masks = self._extract(image)
        if len(masks) != 1:
            return False
        return True
