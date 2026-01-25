from dataclasses import dataclass
from domain.person.snapshot.person_id import DomainPersonSnapshotPersonId
from domain.utils.sequence_base import DomainUtilsSequenceBase

@dataclass(frozen=True)
class DomainPersonSnapshotPersonIdSequence(DomainUtilsSequenceBase[DomainPersonSnapshotPersonId]):
    """
    人物検出結果の人物IDのシーケンスのドメインモデル
    """
    pass
