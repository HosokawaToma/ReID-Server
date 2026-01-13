from applications import ApplicationBase
from domain.person.snapshot.answer_only import DomainPersonSnapshotAnswerOnly
from domain.id_value import DomainIdValue
from domain.person.snapshot.person_id_value import DomainPersonSnapshotPersonIdValue
from dto.person.snapshot.answer_only import DtoPersonSnapshotAnswerOnly
from repositories.person.snapshot.answer_only import RepositoryPersonSnapshotAnswerOnly
from error import Error


class ApplicationPersonSnapshotAnswerNewError(Error):
    pass


class ApplicationPersonSnapshotAnswerNew(ApplicationBase):
    """
    人物画像の正解データを作成する
    :param person_snapshot_id: 人の写真のID
    :return: 人の写真に対する回答
    """
    def __init__(self, repository_person_snapshot_answer: RepositoryPersonSnapshotAnswerOnly):
        self.repository_person_snapshot_answer = repository_person_snapshot_answer

    def new(self, person_snapshot_id: DomainIdValue) -> DtoPersonSnapshotAnswerOnly:
        try:
            answer_only = DomainPersonSnapshotAnswerOnly(
                answer=DomainPersonSnapshotPersonIdValue.new_id(),
                id=DomainIdValue(id=person_snapshot_id.id),
            )
            self.repository_person_snapshot_answer.save(answer_only)
            return DtoPersonSnapshotAnswerOnly(
                id=answer_only.id.id,
                person_id=answer_only.answer.person_id.id if answer_only.answer.person_id is not None else None,
                is_junk=answer_only.answer.is_junk,
            )
        except Error as error:
            raise ApplicationPersonSnapshotAnswerNewError(error) from error
