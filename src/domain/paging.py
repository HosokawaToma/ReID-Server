from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from domain.pagination import DomainPagination

@dataclass(frozen=True)
class DomainPaging(DomainUtilsBase):
    """
    ページングのドメインモデル
    """
    page: int
    search_limit: int

    def offset(self) -> int:
        return (self.page - 1) * self.search_limit
