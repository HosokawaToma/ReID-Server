from applications import ApplicationBase
from domain.person.snapshot.answer_annotation_only import DomainPersonSnapshotAnswerAnnotationOnly
from domain.id_value import DomainIdValue
from domain.person.snapshot.person_id_value import DomainPersonSnapshotPersonIdValue
from value.person.snapshot.annotation import ValuePersonSnapshotAnnotation
from value.id import ValueId
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

    def new(self, person_snapshot_id: DtoId) -> DtoPersonSnapshotAnswerAnnotationOnly:
        try:
            answer_annotation_only = DomainPersonSnapshotAnswerAnnotationOnly(
                answer=ValuePersonSnapshotAnnotation.new_id(),
                id=ValueId(id=person_snapshot_id.id),
            )
            self.repository_person_snapshot_answer.save(answer_annotation_only)
            return DtoPersonSnapshotAnswerAnnotationOnly(
                id=answer_annotation_only.id.id,
                person_id=answer_annotation_only.answer.person_id.id if answer_annotation_only.answer.person_id is not None else None,
                is_junk=answer_annotation_only.answer.is_junk,
            )
        except Error as error:
            raise ApplicationPersonSnapshotAnswerNewError(error) from error
