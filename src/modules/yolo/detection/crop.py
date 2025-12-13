from PIL import Image
from entities.yolo.detection import EntityYoloDetection

class ModuleYoloDetectionCrop:
    def __init__(self):
        pass

    def crop(self, image: Image.Image, detection: EntityYoloDetection) -> Image.Image:
        return image.crop((detection.x1, detection.y1, detection.x2, detection.y2))
