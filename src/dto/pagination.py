"""
ページング用 DTO

総件数と総ページ数を保持する。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoPagination:
    """
    ページング情報を表す DTO。

    :param int total_items: 総件数
    :param int total_pages: 総ページ数
    """
    total_items: int
    total_pages: int
