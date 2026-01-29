from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
import math
from error import ValidationError

@dataclass(frozen=True)
class DomainPagination(DomainUtilsBase):
    """
    ページングのドメインモデル
    """
    total_items: int
    total_pages: int

    @classmethod
    def create(cls, total_items: int, search_limit: int) -> "DomainPagination":
        """
        総件数と検索件数からページングを生成する
        :param int total_items: 総件数
        :param int search_limit: 検索件数
        :return DomainPagination: ページング
        """
        if search_limit <= 0:
            raise ValidationError("search_limit must be greater than 0: {search_limit}")
        if total_items < 0:
            raise ValidationError("total_items must be greater than 0: {total_items}")
        return cls(
            total_items=total_items,
            total_pages=math.ceil(total_items / search_limit),
        )
