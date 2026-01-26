from applications import ApplicationBase
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from domain.id import DomainId
from domain.id_sequence import DomainIdSequence


class ApplicationPersonSnapshotAnswerCopy(ApplicationBase):
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotAnswerCopy":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment=environment),
        )

    def assign_new_person_id(self, person_snapshot_ids: DomainIdSequence) -> DomainId:
        """
        人物検出結果に新しい人物IDを割り当てる
        :param DomainIdSequence person_snapshot_ids: 人物検出結果IDリスト
        :return DomainId: 新しく生成された人物ID
        """
        return self.repository_person_snapshot.assign_new_person_id(person_snapshot_ids=person_snapshot_ids)
