from PIL import Image

class DomainYoloBoundingBox:
    def __init__(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        confidence: float,
        class_id: int,
    ):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.confidence = confidence
        self.class_id = class_id

    def crop(self, image: Image.Image) -> Image.Image:
        cropped_image = image.crop((self.x1, self.y1, self.x2, self.y2))
        cropped_image.format = image.format
        return cropped_image
