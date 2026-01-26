from environment import Environment
from applications import ApplicationBase
from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.person.snapshot.answer.new_id import DtoPersonSnapshotAnswerNewId
from domain.id import DomainId
from domain.person.id import DomainPersonId
from domain.person.snapshot.person_id import DomainPersonSnapshotPersonId


class ApplicationPersonSnapshotAnswerNewId(ApplicationBase):
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotAnswerNewId":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment=environment),
        )

    def update(self, new_id: DtoPersonSnapshotAnswerNewId) -> None:
        """
        人物検出結果の正解ラベルを更新する
        :param DtoPersonSnapshotAnswerNewId new_id: 人物検出結果の正解ラベルの新しいID
        """
        self.repository_person_snapshot.update_answer_label(DomainPersonSnapshotPersonId(
            id=DomainId(id=new_id.person_snapshot_id),
            person_id=DomainPersonId(
                id=DomainId(id=new_id.person_id) if new_id.person_id is not None else None,
                is_junk=new_id.is_junk,
            ),
        ))
