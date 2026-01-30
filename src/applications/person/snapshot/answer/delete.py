from applications import ApplicationBase
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.id import DtoId
from domain.id import DomainId

class ApplicationPersonSnapshotAnswerDelete(ApplicationBase):
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotAnswerDelete":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment=environment),
        )

    def delete(self, person_snapshot_id: DtoId) -> None:
        """
        人物検出結果の正解ラベルを削除する
        :param DtoId person_snapshot_id: 人物検出結果のID
        """
        self.repository_person_snapshot.delete_answer_label_by_id(person_snapshot_id=DomainId(id=person_snapshot_id.id))
