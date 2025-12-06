from PIL import Image
from ultralytics.models.yolo import YOLO
from entities.yolo.mask import EntityYoloMask
from ultralytics.engine.results import Results
from error import Error

class ModuleYoloSegmentationError(Error):
    pass

class ModuleYoloSegmentation:
    def __init__(self):
        self.model = YOLO("./resources/models/yolo11x-seg.pt")

    def extract(self, frame: Image.Image) -> list[EntityYoloMask]:
        results = self.model(frame, classes=[0], verbose=False)
        result: Results = results[0]
        if result.masks is None:
            raise ModuleYoloSegmentationError("yolo segmentation masks is None")
        if len(result.masks) == 0:
            raise ModuleYoloSegmentationError("yolo segmentation masks is empty")
        masks = []
        for mask in result.masks:
            masks.append(EntityYoloMask(result.orig_img, mask.xy.pop()))
        return masks
