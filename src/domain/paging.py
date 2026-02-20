"""
ページング（ページ番号・件数）のドメインモデル

オフセット計算とバリデーションを提供する。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from error import ValidationError


@dataclass(frozen=True)
class DomainPaging(DomainUtilsBase):
    """
    ページングのドメインモデル。

    ページ番号と1ページあたりの件数を保持し、offset でスキップ件数を返す。
    """
    page: int
    search_limit: int

    def __post_init__(self) -> None:
        """
        ページ・件数の妥当性を検証する。0以下は ValidationError。
        """
        if self.page <= 0:
            raise ValidationError("page must be greater than 0: {self.page}")
        if self.search_limit <= 0:
            raise ValidationError(
                "search_limit must be greater than 0: {self.search_limit}")

    def offset(self) -> int:
        """
        現在ページの先頭までのスキップ件数（オフセット）を返す。

        :return int: オフセット
        """
        return (self.page - 1) * self.search_limit
