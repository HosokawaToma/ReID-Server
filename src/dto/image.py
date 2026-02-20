"""
画像 DTO

画像バイト列とフォーマットを保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoImage:
    """
    画像データを保持する DTO。

    API で受け取る画像のバイト列とフォーマット（拡張子）を保持する。

    :param bytes bytes: 画像のバイト列
    :param str format: 画像フォーマット（例: jpg, png）
    """
    bytes: bytes
    format: str
