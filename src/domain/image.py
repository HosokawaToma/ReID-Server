"""
画像のドメインモデル

バイト列とフォーマットを保持し、PIL 画像への変換・クロップを提供する。
"""
from dataclasses import dataclass
from PIL import Image
import io
from domain.utils.base import DomainUtilsBase
from typing import ClassVar


@dataclass(frozen=True)
class DomainImage(DomainUtilsBase):
    """
    画像のドメインモデル。

    バイト列とフォーマットを保持し、許可フォーマット以外は __post_init__ で拒否する。
    """
    bytes: bytes
    format: str
    EXTENSIONS: ClassVar[list[str]] = ["jpg", "jpeg", "png"]

    def __post_init__(self) -> None:
        """
        フォーマットが許可リストに含まれるか検証する。
        """
        if self.format not in self.EXTENSIONS:
            raise ValueError(f"不正なフォーマットです: {self.format}")

    @classmethod
    def from_image(cls, image: Image.Image) -> "DomainImage":
        """
        PIL 画像からドメイン画像を生成する。

        :param Image.Image image: PIL 画像
        :return DomainImage: ドメイン画像
        :raises ValueError: 画像のフォーマットが不明な場合
        """
        if image.format is None:
            raise ValueError("画像のフォーマットが不明です")
        buffer = io.BytesIO()
        image.save(buffer, format=image.format)
        return cls(bytes=buffer.getvalue(), format=image.format.lower())

    @property
    def image(self) -> Image.Image:
        """
        バイト列から PIL 画像を生成して返す。

        :return Image.Image: PIL 画像
        """
        return Image.open(io.BytesIO(self.bytes))

    def crop(self, x1: float, y1: float, x2: float, y2: float) -> "DomainImage":
        """
        指定矩形で画像をクロップした新しい DomainImage を返す。

        :param float x1: 左端
        :param float y1: 上端
        :param float x2: 右端
        :param float y2: 下端
        :return DomainImage: クロップ後の画像
        """
        image = self.image.crop((x1, y1, x2, y2))
        image.format = self.format
        return DomainImage.from_image(image)
