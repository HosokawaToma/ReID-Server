from dataclasses import dataclass

@dataclass(frozen=True)
class DomainDate:
    """
    日付のドメインモデル
    :param datetime date: 日付
    """
    year: int
    month: int
    day: int
