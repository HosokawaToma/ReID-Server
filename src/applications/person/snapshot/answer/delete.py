"""
人物検出結果の正解ラベル削除アプリケーション

指定した人物検出結果IDの正解ラベルを削除する。
"""
from applications import ApplicationBase
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.id import DtoId
from domain.id import DomainId


class ApplicationPersonSnapshotAnswerDelete(ApplicationBase):
    """
    人物検出結果の正解ラベル削除を担当するアプリケーション。

    指定した人物検出結果IDに紐づく正解ラベルを削除する。
    """

    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        """
        アプリケーションを初期化する。

        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        """
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotAnswerDelete":
        """
        環境変数からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境変数
        :return ApplicationPersonSnapshotAnswerDelete: アプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment=environment),
        )

    def delete(self, person_snapshot_id: DtoId) -> None:
        """
        指定した人物検出結果に紐づく正解ラベルを削除する。

        :param DtoId person_snapshot_id: 対象の人物検出結果のID
        """
        self.repository_person_snapshot.delete_answer_label_by_id(
            person_snapshot_id=DomainId(id=person_snapshot_id.id))
