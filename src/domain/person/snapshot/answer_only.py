from dataclasses import dataclass, field
from domain.id_value import DomainIdValue
from domain.person.snapshot.person_id_value import DomainPersonSnapshotPersonIdValue

@dataclass
class DomainPersonSnapshotAnswerOnly:
    """
    人物画像の正解データに関するドメイン知識を集約する
    :param DomainPersonSnapshotPersonIdValue answer: 人物ID
    :param DomainIdValue id: 人物画像のID
    """
    answer: DomainPersonSnapshotPersonIdValue
    id: DomainIdValue = field(default_factory=DomainIdValue)
