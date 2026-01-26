from environment import Environment
from applications import ApplicationBase
from repositories.person.snapshot import RepositoryPersonSnapshot
from domain.id import DomainId
from domain.person.id import DomainPersonId
from domain.person.snapshot.person_id import DomainPersonSnapshotPersonId
from domain.person.snapshot.person_id_sequence import DomainPersonSnapshotPersonIdSequence
import uuid


class ApplicationPersonSnapshotAnswerNewId(ApplicationBase):
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotAnswerNewId":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment=environment),
        )

    def update(self, person_snapshot_ids: list[uuid.UUID], person_id: uuid.UUID | None, is_junk: bool) -> None:
        """
        人物検出結果の正解ラベルを更新する
        :param list[uuid.UUID] person_snapshot_ids: 人物検出結果のIDリスト
        :param uuid.UUID | None person_id: 正解人物のID（ゴミデータの場合はNone）
        :param bool is_junk: 正解人物がゴミデータかどうか
        """
        person_snapshot_person_ids = DomainPersonSnapshotPersonIdSequence(items=[
            DomainPersonSnapshotPersonId(
                id=DomainId(id=person_snapshot_id),
                person_id=DomainPersonId(
                    id=DomainId(id=person_id) if person_id is not None else None,
                    is_junk=is_junk,
                ),
            ) for person_snapshot_id in person_snapshot_ids
        ])
        self.repository_person_snapshot.update_answer_labels_batch(person_snapshot_person_ids)
