from abc import ABC
from typing import TypeVar
from sqlalchemy.orm import Query
from domain.paging import DomainPaging

T = TypeVar("T")


class RepositoryUtilBase(ABC):
    def _apply_paging(self, query: Query[T], paging: DomainPaging) -> Query[T]:
        """
        ページングを適用する。
        :param Query[Any] query: クエリ
        :param DomainPaging paging: ページング
        :return Query[Any]: ページングが適用されたクエリ
        """
        return query.limit(paging.search_limit).offset(paging.offset())
