"""
ページング（ページ番号・件数）のドメインモデル

「何ページ目を」「1 ページあたり何件」取得するかを表し、DB の LIMIT/OFFSET に対応する
スキップ件数の計算と、不正な値の拒否を行う。
"""
from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from error import ValidationError


@dataclass(frozen=True)
class DomainPaging(DomainUtilsBase):
    """
    ページングのドメインモデル。

    ページ番号は 1 始まり。1 ページあたりの最大件数は 1 以上である必要がある。
    いずれかが 0 以下の場合は ValidationError となる。
    先頭からスキップする件数は「（ページ番号 − 1）× 1 ページあたり件数」で与えられ、1 ページ目では 0 となる。
    """
    page: int
    search_limit: int

    def __post_init__(self) -> None:
        """
        ページ番号および 1 ページあたり件数が 1 以上であることを検証する。
        どちらかが 0 以下の場合は ValidationError。
        """
        if self.page <= 0:
            raise ValidationError("page must be greater than 0: {self.page}")
        if self.search_limit <= 0:
            raise ValidationError(
                "search_limit must be greater than 0: {self.search_limit}")

    def offset(self) -> int:
        """
        現在のページの先頭までにスキップすべき件数を返す。

        1 ページ目では 0、2 ページ目では 1 ページあたり件数と等しい。

        :return int: スキップ件数（0 以上）
        """
        return (self.page - 1) * self.search_limit
