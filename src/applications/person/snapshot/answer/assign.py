"""
人物検出結果の正解ラベル割当アプリケーション

ソース人物検出結果の正解ラベルをターゲットにコピーする。
"""
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
    """
    人物検出結果の正解ラベル割当を担当するアプリケーション。

    ソース人物検出結果の正解ラベル（人物ID）をターゲット複数件にコピーする。ソースに正解が無い場合は新規作成してからコピーする。
    """

    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        """
        アプリケーションを初期化する。

        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        """
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotAnswerAssign":
        """
        環境変数からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境変数
        :return ApplicationPersonSnapshotAnswerAssign: アプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment=environment),
        )

    def assign_person_id(
        self,
        source_person_snapshot_id: DtoId,
        target_person_snapshot_ids: list[DtoId],
    ) -> None:
        """
        ソース1件の正解ラベルをターゲット複数件に割り当てる。ソースに正解が無い場合は新規の人物IDで正解を作成してから割り当てる。

        :param DtoId source_person_snapshot_id: 正解の参照元となる人物検出結果のID
        :param list[DtoId] target_person_snapshot_ids: 正解を付与する人物検出結果のIDリスト
        """
        try:
            source_answer_label = self.repository_person_snapshot.find_answer_label_by_id(
                person_snapshot_id=DomainId(id=source_person_snapshot_id.id)
            )
        except NotFoundError:
            source_answer_label = DomainPersonSnapshotPersonId(
                id=DomainId(id=source_person_snapshot_id.id),
                person_id=DomainPersonId.new_id(),
            )
            self.repository_person_snapshot.add_answer_label(
                source_answer_label)
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
