from dataclasses import dataclass
from domain.image import DomainImage
from domain.utils.base import DomainUtilsBase

@dataclass
class DomainYoloBoundingBox(DomainUtilsBase):
    """
    YOLOのバウンディングボックスのドメインモデル
    """
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    class_id: int

    def crop(self, image: DomainImage) -> DomainImage:
        return image.crop(self.x1, self.y1, self.x2, self.y2)
