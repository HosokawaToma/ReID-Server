from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase

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
        return cls(
            total_items=total_items,
            total_pages=int(total_items / search_limit),
        )
