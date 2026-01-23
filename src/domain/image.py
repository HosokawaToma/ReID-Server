from dataclasses import dataclass
from PIL import Image
import io
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainImage(DomainUtilsBase):
    """
    画像のドメインモデル
    """
    bytes: bytes
    format: str

    @classmethod
    def from_image(cls, image: Image.Image) -> "DomainImage":
        if image.format is None:
            raise ValueError("画像のフォーマットが不明です")
        buffer = io.BytesIO()
        image.save(buffer, format=image.format)
        return cls(bytes=buffer.getvalue(), format=image.format)

    @property
    def image(self) -> Image.Image:
        return Image.open(io.BytesIO(self.bytes))

    def crop(self, x1: float, y1: float, x2: float, y2: float) -> "DomainImage":
        image = self.image.crop((x1, y1, x2, y2))
        image.format = self.format
        return DomainImage.from_image(image)
