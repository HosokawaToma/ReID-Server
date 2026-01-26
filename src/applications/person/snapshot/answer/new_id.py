from environment import Environment
from applications import ApplicationBase
from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.id import DtoId
from dto.person.id import DtoPersonId
from domain.id import DomainId
from domain.person.id import DomainPersonId
from domain.person.snapshot.person_id import DomainPersonSnapshotPersonId
from domain.person.snapshot.person_id_sequence import DomainPersonSnapshotPersonIdSequence


class ApplicationPersonSnapshotAnswerNewId(ApplicationBase):
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotAnswerNewId":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment=environment),
        )

    def new_id(self, person_snapshot_ids: list[DtoId], person_id: DtoPersonId) -> None:
        """
        人物検出結果の正解ラベルを更新する
        :param list[DtoId] person_snapshot_ids: 人物検出結果のIDリスト
        :param DtoPersonId person_id: 正解人物のID
        """
        # person_idがNoneでis_junkがFalseの場合、新しいIDを生成
        if person_id.id is None and not person_id.is_junk:
            domain_person_id = DomainPersonId().new_id()
        else:
            domain_person_id = DomainPersonId(
                id=DomainId(id=person_id.id) if person_id.id is not None else None,
                is_junk=person_id.is_junk,
            )
        
        person_snapshot_person_ids = DomainPersonSnapshotPersonIdSequence(items=[
            DomainPersonSnapshotPersonId(
                id=DomainId(id=person_snapshot_id.id),
                person_id=domain_person_id,
            ) for person_snapshot_id in person_snapshot_ids
        ])
        self.repository_person_snapshot.update_answer_labels_batch(person_snapshot_person_ids)
