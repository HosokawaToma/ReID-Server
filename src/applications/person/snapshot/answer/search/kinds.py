from applications import ApplicationBase
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.person.snapshot.person_id import DtoPersonSnapshotPersonId

class ApplicationPersonSnapshotAnswerSearchKinds(ApplicationBase):
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotAnswerSearchKinds":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment=environment),
        )

    def search(self) -> list[DtoPersonSnapshotPersonId]:
        """
        人物検出結果の正解ラベルの種類を検索する
        :return list[DtoPersonSnapshotPersonId]: 人物検出結果の正解ラベルの種類リスト
        :raises ApplicationPersonSnapshotAnswerSearchKindsError: 人物検出結果の正解ラベルの種類検索に失敗した場合に発生するエラー
        """
        answer_label_kinds = self.repository_person_snapshot.find_answer_label_kinds()
        return [DtoPersonSnapshotPersonId(
                id=answer_label_kind.id.id,
                person_id=answer_label_kind.person_id.id.id if answer_label_kind.person_id.id is not None else None,
                is_junk=answer_label_kind.person_id.is_junk,
            ) for answer_label_kind in answer_label_kinds]
