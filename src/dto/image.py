from dataclasses import dataclass
from PIL import Image

@dataclass
class DtoImage:
    """
    画像データを表すDTO
    :param Image.Image image: 画像
    """
    image: Image.Image
