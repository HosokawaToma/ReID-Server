"""
人物検出結果の正解ラベル検索アプリケーション

クエリ条件に応じて正解ラベル一覧を取得する。
"""
from applications import ApplicationBase
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.person.snapshot.answer.query import DtoPersonSnapshotAnswerQuery
from dto.person.snapshot.person_id import DtoPersonSnapshotPersonId
from repositories.utils.database.query.person_snapshot_answer_label import RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabel
from repositories.utils.database.query.person_snapshot_answer_label import RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabelSortByKey


class ApplicationPersonSnapshotAnswerSearch(ApplicationBase):
    """
    人物検出結果の正解ラベルを検索するアプリケーションクラス。
    """

    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        """
        アプリケーションを初期化する。

        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        """
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotAnswerSearch":
        """
        環境からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return ApplicationPersonSnapshotAnswerSearch: アプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment=environment),
        )

    def search(self, query: DtoPersonSnapshotAnswerQuery | None = None) -> list[DtoPersonSnapshotPersonId]:
        """
        人物検出結果の正解ラベルを検索する
        :param DtoPersonSnapshotAnswerQuery query: クエリ
        :return list[DtoPersonSnapshotPersonId]: 人物検出結果の正解ラベルリスト
        :raises ApplicationPersonSnapshotAnswerSearchError: 人物検出結果の正解ラベル検索に失敗した場合に発生するエラー
        """
        database_query = None
        if query is not None:
            database_query = RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabel(
                person_snapshot_ids=query.person_snapshot_ids,
                person_ids=query.person_ids,
                is_junk=query.is_junk,
                sort_by_list=[
                    RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabelSortByKey(
                        sort_by.value)
                    for sort_by in query.sort_by_list
                ] if query.sort_by_list is not None else None,
            )
        answer_labels = self.repository_person_snapshot.find_answer_labels(
            query=database_query)
        return [DtoPersonSnapshotPersonId(
            id=answer_label.id.id,
            person_id=answer_label.person_id.id.id if answer_label.person_id.id is not None else None,
            is_junk=answer_label.person_id.is_junk,
        ) for answer_label in answer_labels]
