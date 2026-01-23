from applications import ApplicationBase
from repositories.person.snapshot.answer_annotation_only import RepositoryPersonSnapshotAnswerAnnotationOnly
from dto.id import DtoId
from dto.person.snapshot.answer_annotation_only import DtoPersonSnapshotAnswerAnnotationOnly
from value.id_sequence import ValueIdSequence
from value.id import ValueId
from error import Error


class ApplicationPersonSnapshotAnswerCopyError(Error):
    pass


class ApplicationPersonSnapshotAnswerCopy(ApplicationBase):
    def __init__(self, repository_person_snapshot_answer: RepositoryPersonSnapshotAnswerAnnotationOnly):
        self.repository_person_snapshot_answer = repository_person_snapshot_answer

    def copy(self, source_person_snapshot_id: DtoId, target_person_snapshot_ids: list[DtoId]) -> list[DtoPersonSnapshotAnswerAnnotationOnly]:
        try:
            source_answer_annotation = self.repository_person_snapshot_answer.find_by_person_snapshot_id(ValueId(id=source_person_snapshot_id.id))
            target_answer_annotations = self.repository_person_snapshot_answer.find_by_person_snapshot_ids(ValueIdSequence.from_iterable(target_person_snapshot_ids))
            target_answer_annotations.everything_annotation_copy(source_answer_annotation.answer)
            self.repository_person_snapshot_answer.save_all(target_answer_annotations)
            return [
                DtoPersonSnapshotAnswerAnnotationOnly(
                    id=answer_annotation.id.id,
                    person_id=answer_annotation.answer.person_id.id if answer_annotation.answer.person_id is not None else None,
                    is_junk=answer_annotation.answer.is_junk,
                )
                for answer_annotation in target_answer_annotations
            ]
        except Error as error:
            raise ApplicationPersonSnapshotAnswerCopyError(error) from error
