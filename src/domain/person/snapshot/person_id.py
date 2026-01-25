from dataclasses import dataclass
from domain.person.id import DomainPersonId
from domain.utils.base import DomainUtilsBase
from domain.id import DomainId

@dataclass(frozen=True)
class DomainPersonSnapshotPersonId(DomainUtilsBase):
    """
    人物検出結果の人物IDのドメインモデル
    """
    id: DomainId
    person_id: DomainPersonId
