from PIL import Image
from ultralytics.models.yolo import YOLO
from entities.yolo.mask import EntityYoloMask
from ultralytics.engine.results import Results


class ModuleYoloSegmentation:
    def __init__(self):
        self.model = YOLO("models/yolo11x-seg.pt")

    def extract(self, frame: Image.Image) -> list[EntityYoloMask]:
        results = self.model(frame, classes=[0], verbose=False)
        result: Results = results[0]
        if result.masks is None:
            return []
        masks = []
        for mask in result.masks:
            masks.append(EntityYoloMask(result.orig_img, mask.xy.pop()))
        return masks
