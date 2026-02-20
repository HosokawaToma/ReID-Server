"""
ページング（総件数・総ページ数）のドメインモデル

検索結果の総件数と、1 ページあたり件数から総ページ数を算出し、クライアントに
「全体で何件・何ページあるか」を返すために用いる。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
import math
from error import ValidationError


@dataclass(frozen=True)
class DomainPagination(DomainUtilsBase):
    """
    ページング情報（総件数・総ページ数）のドメインモデル。

    総件数は検索条件に一致する件数全体。総ページ数は総件数を 1 ページあたり件数で割った値の切り上げで与える。
    総件数が 0 のとき、総ページ数は 0 となる。
    """
    total_items: int
    total_pages: int

    @classmethod
    def create(cls, total_items: int, search_limit: int) -> "DomainPagination":
        """
        総件数と 1 ページあたり件数から、総件数・総ページ数を保持したインスタンスを生成する。

        総ページ数は「総件数 ÷ 1 ページあたり件数」の切り上げで計算する。
        1 ページあたり件数が 0 以下、または総件数が負の場合は ValidationError。

        :param int total_items: 検索結果の総件数（0 以上）
        :param int search_limit: 1 ページあたりの件数（1 以上）
        :return DomainPagination: 総件数と総ページ数を保持したインスタンス
        :raises ValidationError: 1 ページあたり件数が 0 以下、または総件数が負の場合
        """
        if search_limit <= 0:
            raise ValidationError(
                f"search_limit must be greater than 0: {search_limit}")
        if total_items < 0:
            raise ValidationError(
                f"total_items must be greater than or equal to 0: {total_items}")
        return cls(
            total_items=total_items,
            total_pages=math.ceil(total_items / search_limit),
        )
