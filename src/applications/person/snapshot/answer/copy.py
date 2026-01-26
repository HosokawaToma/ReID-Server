from applications import ApplicationBase
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from domain.id import DomainId
from domain.id_sequence import DomainIdSequence
from domain.person.id import DomainPersonId
from domain.person.snapshot.person_id import DomainPersonSnapshotPersonId
from domain.person.snapshot.person_id_sequence import DomainPersonSnapshotPersonIdSequence
from error import NotFoundError


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
        :raises NotFoundError: 指定されたperson_snapshot_idが存在しない場合
        """
        self._validate_person_snapshots_exist(person_snapshot_ids)
        
        new_person_id = DomainPersonId().new_id()
        
        person_snapshot_person_ids = DomainPersonSnapshotPersonIdSequence(items=[
            DomainPersonSnapshotPersonId(
                id=snapshot_id,
                person_id=new_person_id
            )
            for snapshot_id in person_snapshot_ids.items
        ])
        
        self.repository_person_snapshot.update_answer_labels(
            person_snapshot_person_ids=person_snapshot_person_ids
        )
        
        return new_person_id.id

    def _validate_person_snapshots_exist(self, person_snapshot_ids: DomainIdSequence) -> None:
        """
        人物検出結果が存在するかを検証する
        :param DomainIdSequence person_snapshot_ids: 人物検出結果IDリスト
        :raises NotFoundError: 指定されたperson_snapshot_idが存在しない場合
        """
        existing_ids = self.repository_person_snapshot.find_ids()
        existing_id_set = {existing_id.id for existing_id in existing_ids.items}
        
        missing_ids = [snapshot_id.id for snapshot_id in person_snapshot_ids.items if snapshot_id.id not in existing_id_set]
        
        if missing_ids:
            raise NotFoundError(f"指定された人物検出結果が見つかりません: {missing_ids}")
