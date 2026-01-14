from domain.utils.sequence import DomainUtilsSequenceBase
from domain.person.snapshot.answer_annotation_only import DomainPersonSnapshotAnswerAnnotationOnly
from value.id import ValueId
from value.person.snapshot.annotation import ValuePersonSnapshotAnnotation

class DomainPersonSnapshotAnswerAnnotationOnlySequence(DomainUtilsSequenceBase[DomainPersonSnapshotAnswerAnnotationOnly]):
    def everything_new_person_id(self) -> "DomainPersonSnapshotAnswerAnnotationOnlySequence":
        person_id = ValueId()
        for item in self.items:
            item.answer.person_id = person_id
        return self

    def everything_annotation_copy(self, annotation: ValuePersonSnapshotAnnotation) -> "DomainPersonSnapshotAnswerAnnotationOnlySequence":
        for item in self.items:
            item.answer.copy(annotation)
        return self
