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

    def copy(self, source_id: DomainId, target_ids: DomainIdSequence) -> None:
        """
        人物検出結果の正解ラベルをコピーする
        :param DomainId source_id: コピー元の人物検出結果ID
        :param DomainIdSequence target_ids: コピー先の人物検出結果IDリスト
        :raises NotFoundError: コピー元の正解ラベルが見つからない場合に発生するエラー
        """
        self.repository_person_snapshot.copy_answer_label(source_id=source_id, target_ids=target_ids)
