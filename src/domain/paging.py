from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from error import ValidationError

@dataclass(frozen=True)
class DomainPaging(DomainUtilsBase):
    """
    ページングのドメインモデル
    """
    page: int
    search_limit: int

    def __post_init__(self):
        if self.page <= 0:
            raise ValidationError("page must be greater than 0: {self.page}")
        if self.search_limit <= 0:
            raise ValidationError("search_limit must be greater than 0: {self.search_limit}")

    def offset(self) -> int:
        return (self.page - 1) * self.search_limit
