"""
人物検出正解ラベル用データベースクエリビルダ

person_snapshots_answer_labels テーブルに対する条件・ソートを組み立てる。
"""
from dataclasses import dataclass
from sqlalchemy.orm import Query
from migration.models.person_snapshots_answer_labels import MigrationModelPersonSnapshotsAnswerLabels
import uuid
from enum import Enum


class RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabelSortByKey(Enum):
    """正解ラベルクエリのソートキー。"""
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"


@dataclass
class RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabel:
    """
    正解ラベルテーブル用のクエリ条件を保持するデータクラス。

    人物検出ID・人物ID・ゴミフラグ・ソート順を保持し、SQLAlchemy の Query にフィルタと ORDER BY を適用した結果を返す。
    """
    person_snapshot_ids: list[uuid.UUID] | None = None
    person_ids: list[uuid.UUID] | None = None
    is_junk: bool | None = None
    sort_by_list: list[RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabelSortByKey] | None = None

    def build(
        self,
        session_query: Query[MigrationModelPersonSnapshotsAnswerLabels],
    ) -> Query[MigrationModelPersonSnapshotsAnswerLabels]:
        """
        保持する条件をベースクエリに適用し、フィルタ・ソートを付けたクエリを返す。条件が None の項目は適用しない。

        :param Query[MigrationModelPersonSnapshotsAnswerLabels] session_query: ベースとなるクエリ
        :return Query[MigrationModelPersonSnapshotsAnswerLabels]: 条件を適用したクエリ
        """
        if self.person_snapshot_ids is not None:
            session_query = session_query.filter(
                MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id.in_(self.person_snapshot_ids))
        if self.person_ids is not None:
            session_query = session_query.filter(
                MigrationModelPersonSnapshotsAnswerLabels.person_id.in_(self.person_ids))
        if self.is_junk is not None:
            session_query = session_query.filter(
                MigrationModelPersonSnapshotsAnswerLabels.is_junk == self.is_junk)
        if self.sort_by_list is not None:
            for sort_by in self.sort_by_list:
                if sort_by == RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabelSortByKey.CREATED_AT_ASC:
                    session_query = session_query.order_by(
                        MigrationModelPersonSnapshotsAnswerLabels.created_at.asc())
                elif sort_by == RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabelSortByKey.CREATED_AT_DESC:
                    session_query = session_query.order_by(
                        MigrationModelPersonSnapshotsAnswerLabels.created_at.desc())
        return session_query
