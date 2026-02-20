"""
画像のドメインモデル

画像データをバイト列とフォーマット（拡張子）で保持し、PIL 画像への変換と矩形クロップを提供する。
許可するフォーマットは jpg / jpeg / png に限定され、それ以外は受け付けない。
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

    画像の実体をバイト列で、形式を小文字の拡張子文字列で保持する。
    許可形式は jpg / jpeg / png のみ。それ以外は ValueError となる。
    バイト列から PIL 画像を取得する仕組みは読み取り専用の利用を想定している。
    """
    bytes: bytes
    format: str
    EXTENSIONS: ClassVar[list[str]] = ["jpg", "jpeg", "png"]

    def __post_init__(self) -> None:
        """
        フォーマットが jpg / jpeg / png のいずれかであることを検証する。違う場合は ValueError。
        """
        if self.format not in self.EXTENSIONS:
            raise ValueError(f"不正なフォーマットです: {self.format}")

    @classmethod
    def from_image(cls, image: Image.Image) -> "DomainImage":
        """
        PIL 画像からドメイン画像を生成する。

        画像をメモリ上でバイト列にシリアライズし、形式は元画像のフォーマットを小文字にした値とする。
        元画像のフォーマットが不明な場合は ValueError となる。

        :param Image.Image image: 元となる PIL 画像
        :return DomainImage: 同一内容をバイト列で保持したドメイン画像
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
        保持しているバイト列から PIL 画像を生成して返す。

        返却された画像を変更しても、このドメイン画像が保持するバイト列には反映されない。

        :return Image.Image: このドメイン画像の内容を表す PIL 画像
        """
        return Image.open(io.BytesIO(self.bytes))

    def crop(self, x1: float, y1: float, x2: float, y2: float) -> "DomainImage":
        """
        指定した矩形領域で画像をクロップした新しいドメイン画像を返す。

        矩形は左上 (x1, y1) から右下 (x2, y2) まで。左端・上端は含み、右端・下端は含まない半開区間とする。
        元のインスタンスは変更されず、クロップ結果だけが新規インスタンスとして返る。

        :param float x1: クロップ領域の左端（X 座標）
        :param float y1: クロップ領域の上端（Y 座標）
        :param float x2: クロップ領域の右端（X 座標）
        :param float y2: クロップ領域の下端（Y 座標）
        :return DomainImage: クロップ後の画像を保持する新しいドメイン画像
        """
        image = self.image.crop((x1, y1, x2, y2))
        image.format = self.format
        return DomainImage.from_image(image)
