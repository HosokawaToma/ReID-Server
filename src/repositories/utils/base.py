"""
リポジトリユーティリティ基底

ページング適用など、リポジトリで共通利用する処理を提供する。
"""
from abc import ABC
from typing import TypeVar
from sqlalchemy.orm import Query
from domain.paging import DomainPaging

T = TypeVar("T")


class RepositoryUtilBase(ABC):
    """
    リポジトリの抽象基底クラス。

    ページングの適用など、共通メソッドを定義する。
    """

    def _apply_paging(self, query: Query[T], paging: DomainPaging) -> Query[T]:
        """
        1 ページあたり件数とオフセットをクエリに適用し、LIMIT / OFFSET 付きのクエリを返す。

        :param Query[T] query: ベースとなるクエリ
        :param DomainPaging paging: ページ番号と1ページあたり件数
        :return Query[T]: LIMIT と OFFSET が設定されたクエリ
        """
        return query.limit(paging.search_limit).offset(paging.offset())
