from dataclasses import dataclass
from domain.utils.base import DomainUtilsBase
from domain.id import DomainId

@dataclass(frozen=True)
class DomainReidRank(DomainUtilsBase):
    """
    再識別評価のランクのドメインモデル
    人物検出結果のIDとランクを保持する
    :param DomainId id: 人物検出結果のID
    :param int rank: ランク
    """
    id: DomainId
    rank: int
