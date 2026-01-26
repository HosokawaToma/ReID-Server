from applications import ApplicationBase
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from domain.id import DomainId
from domain.id_sequence import DomainIdSequence
import uuid


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
        # 新しい人物IDを生成
        new_person_id = DomainId(id=uuid.uuid4())
        
        # Repository層を使ってラベルを更新
        self.repository_person_snapshot.update_answer_labels(
            person_snapshot_ids=person_snapshot_ids,
            person_id=new_person_id,
            is_junk=False
        )
        
        return new_person_id
