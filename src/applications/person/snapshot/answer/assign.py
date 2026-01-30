from applications import ApplicationBase
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.id import DtoId
from domain.id import DomainId
from domain.person.id import DomainPersonId
from domain.person.snapshot.person_id import DomainPersonSnapshotPersonId
from domain.person.snapshot.person_id_sequence import DomainPersonSnapshotPersonIdSequence
from error import NotFoundError

class ApplicationPersonSnapshotAnswerAssign(ApplicationBase):
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotAnswerAssign":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment=environment),
        )

    def assign(
        self,
        source_person_snapshot_id: DtoId,
        target_person_snapshot_ids: list[DtoId],
    ) -> None:
        """
        ソース人物検出結果の正解ラベルをターゲット人物検出結果に割り当てる
        ソース人物検出結果に正解ラベルが存在しない場合，新たに正解ラベルを作成する
        :param DtoId source_person_snapshot_id: ソース人物検出結果ID
        :param list[DtoId] target_person_snapshot_ids: ターゲット人物検出結果IDリスト
        """
        try:
            source_answer_label = self.repository_person_snapshot.find_answer_label_by_id(
                person_snapshot_id=DomainId(id=source_person_snapshot_id.id)
            )
        except NotFoundError:
            source_answer_label = DomainPersonSnapshotPersonId(
                id=DomainId(id=source_person_snapshot_id.id),
                person_id=DomainPersonId(id=None),
            )
        self.repository_person_snapshot.save_answer_labels(
            DomainPersonSnapshotPersonIdSequence(
                items=[
                    DomainPersonSnapshotPersonId(
                        id=DomainId(id=target_person_snapshot_id.id),
                        person_id=source_answer_label.person_id,
                    ) for target_person_snapshot_id in target_person_snapshot_ids
                ],
            ),
        )
