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
    人物検出結果の正解ラベル検索を担当するアプリケーション。

    クエリ条件（人物検出ID・人物ID・ゴミフラグ・ソート）に応じて正解ラベル（人物検出ID・人物ID・ゴミフラグ）のリストを返す。
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
        クエリ条件に合う正解ラベル（人物検出ID・人物ID・ゴミフラグ）のリストを返す。条件が None の場合は全件を対象とする。

        :param DtoPersonSnapshotAnswerQuery | None query: 検索条件（省略時は全件）
        :return list[DtoPersonSnapshotPersonId]: 正解ラベルDTOのリスト
        :raises InternalServerError: 検索処理に失敗した場合
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
