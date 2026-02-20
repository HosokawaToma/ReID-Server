"""
画像 DTO

画像バイト列とフォーマットを保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoImage:
    """
    画像データを表すDTO
    :param bytes: 画像データ
    :param format: 画像フォーマット
    """
    bytes: bytes
    format: str
