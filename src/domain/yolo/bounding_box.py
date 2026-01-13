from PIL import Image
from dataclasses import dataclass

@dataclass
class DomainYoloBoundingBox:
    """
    物体検出のBounding Boxに関するドメイン知識を集約する
    :param int class_id: クラスID
    :param float confidence: 信頼度
    :param float x1: x座標
    :param float y1: y座標
    :param float x2: x座標
    :param float y2: y座標
    :param int original_x1: 元の画像のx座標
    :param int original_y1: 元の画像のy座標
    :param int original_x2: 元の画像のx座標
    :param int original_y2: 元の画像のy座標
    :param int original_width: 元の画像の幅
    :param int original_height: 元の画像の高さ
    """
    class_id: int
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float
    original_x1: int
    original_y1: int
    original_x2: int
    original_y2: int
    original_width: int
    original_height: int

    def crop(self, image: Image.Image) -> Image.Image:
        cropped_image = image.crop((self.x1, self.y1, self.x2, self.y2))
        cropped_image.format = image.format
        return cropped_image
