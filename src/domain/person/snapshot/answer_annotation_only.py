from dataclasses import dataclass, field
from value.id import ValueId
from value.person.snapshot.annotation import ValuePersonSnapshotAnnotation

@dataclass
class DomainPersonSnapshotAnswerAnnotationOnly:
    """
    人物画像の正解データに関するドメイン知識を集約する
    :param ValuePersonSnapshotAnnotation answer: 人物画像の正解データ
    :param ValueId id: 人物画像のID
    """
    answer: ValuePersonSnapshotAnnotation
    id: ValueId = field(default_factory=ValueId)
