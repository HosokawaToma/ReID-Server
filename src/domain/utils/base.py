from abc import ABC
from dataclasses import dataclass
from error import Error


class DomainUtilsBaseError(Error):
    pass

@dataclass(frozen=True)
class DomainUtilsBase(ABC):
    """
    ドメインモデルのベースクラス
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"
