"""
ページング用 DTO

API のレスポンスで「検索結果の総件数」と「総ページ数」を返すために用いる。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DtoPagination:
    """
    ページング情報を保持する DTO。

    検索条件に一致した件数全体と、1 ページあたり件数から求めた総ページ数を保持する。

    :param int total_items: 総件数
    :param int total_pages: 総ページ数
    """
    total_items: int
    total_pages: int
