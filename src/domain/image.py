from dataclasses import dataclass
from PIL import Image

@dataclass
class DomainImage:
    """
    画像に関するドメイン知識を集約する
    :param Image.Image image: 画像
    """
    image: Image.Image
