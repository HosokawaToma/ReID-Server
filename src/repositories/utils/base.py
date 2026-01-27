from abc import ABC
from typing import Any, TypeVar
from sqlalchemy.orm import Query
from environment import Environment

T = TypeVar("T")

class RepositoryUtilBase(ABC):
    def __init__(self, search_limit: int):
        self.search_limit = search_limit

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryUtilBase":
        return cls(
            search_limit=environment.search_limit,
        )


    def _apply_paging(self, query: Query[T], offset: int = 0) -> Query[T]:
        """
        ページングを適用する。
        :param Query[Any] query: クエリ
        :param int offset: オフセット
        :return Query[Any]: ページングが適用されたクエリ
        """
        return query.limit(self.search_limit).offset(offset)
