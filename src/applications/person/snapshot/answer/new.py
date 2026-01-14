from applications import ApplicationBase
from value.id_sequence import ValueIdSequence
from dto.person.snapshot.answer_annotation_only import DtoPersonSnapshotAnswerAnnotationOnly
from dto.id import DtoId
from repositories.person.snapshot.answer_annotation_only import RepositoryPersonSnapshotAnswerAnnotationOnly
from error import Error


class ApplicationPersonSnapshotAnswerNewError(Error):
    pass


class ApplicationPersonSnapshotAnswerNew(ApplicationBase):
    """
    人物画像の正解データを作成する
    :param person_snapshot_id: 人の写真のID
    :return: 人の写真に対する回答
    """
    def __init__(self, repository_person_snapshot_answer: RepositoryPersonSnapshotAnswerAnnotationOnly):
        self.repository_person_snapshot_answer = repository_person_snapshot_answer

    def new(self, person_snapshot_id: list[DtoId]) -> list[DtoPersonSnapshotAnswerAnnotationOnly]:
        try:
            ids = ValueIdSequence.from_iterable(person_snapshot_id)
            answer_annotations = ids.to_person_snapshot_answer_annotation_only()
            self.repository_person_snapshot_answer.save_all(answer_annotations)
            return [
                DtoPersonSnapshotAnswerAnnotationOnly(
                    id=answer_annotation.id.id,
                    person_id=answer_annotation.answer.person_id.id if answer_annotation.answer.person_id is not None else None,
                    is_junk=answer_annotation.answer.is_junk,
                )
                for answer_annotation in answer_annotations
            ]
        except Error as error:
            raise ApplicationPersonSnapshotAnswerNewError(error) from error
