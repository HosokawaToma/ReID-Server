from value.utils.sequence import ValueUtilsSequenceBase
from domain.person.snapshot.answer_annotation_only import DomainPersonSnapshotAnswerAnnotationOnly
from domain.person.snapshot.answer_annotation_only_sequence import DomainPersonSnapshotAnswerAnnotationOnlySequence
from value.id import ValueId
from value.person.snapshot.annotation import ValuePersonSnapshotAnnotation
from typing import Iterable, Any


class ValueIdSequence(ValueUtilsSequenceBase[ValueId]):
    @classmethod
    def form_iterable(cls, items: Iterable[Any]) -> "ValueIdSequence":
        return cls(items=[ValueId(id=item.id) for item in items])

    def to_person_snapshot_answer_annotation_only(self) -> DomainPersonSnapshotAnswerAnnotationOnlySequence:
        return DomainPersonSnapshotAnswerAnnotationOnlySequence(
            items=[
                DomainPersonSnapshotAnswerAnnotationOnly(
                    id=id,
                    answer=ValuePersonSnapshotAnnotation()
                )
                for id in self.items
            ],
        )
