"""
人物検出結果用データベースクエリビルダ

person_snapshots テーブルに対する条件・ソートを組み立てる。
"""
from dataclasses import dataclass
import uuid
from datetime import datetime
from sqlalchemy.orm import Query
from migration.models.person_snapshots import MigrationModelPersonSnapshot

from enum import Enum


class RepositoryUtilDatabaseQueryPersonSnapshotSortByKey(str, Enum):
    """人物検出結果クエリのソートキー。"""
    TIMESTAMP_ASC = "timestamp_asc"
    TIMESTAMP_DESC = "timestamp_desc"

    def __str__(self) -> str:
        return self.value


@dataclass
class RepositoryUtilDatabaseQueryPersonSnapshot:
    """
    人物検出結果テーブル用のクエリ条件を保持するデータクラス。

    ID・カメラ・ビュー・時刻範囲・ゴミフラグ・人物ID・ソート順を保持し、SQLAlchemy の Query にフィルタと ORDER BY を適用した結果を返す。
    """
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    is_junk: bool | None = None
    person_ids: list[uuid.UUID] | None = None
    sort_by_list: list[RepositoryUtilDatabaseQueryPersonSnapshotSortByKey] | None = None

    def build(self, query: Query[MigrationModelPersonSnapshot]) -> Query[MigrationModelPersonSnapshot]:
        """
        保持する条件をベースクエリに適用し、フィルタ・ソートを付けたクエリを返す。条件が None の項目は適用しない。

        :param Query[MigrationModelPersonSnapshot] query: ベースとなるクエリ
        :return Query[MigrationModelPersonSnapshot]: 条件を適用したクエリ
        """
        if self.ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.id.in_(self.ids))
        if self.camera_ids is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.camera_id.in_(self.camera_ids))
        if self.view_ids is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.view_id.in_(self.view_ids))
        if self.timestamp_after is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.timestamp >= self.timestamp_after)
        if self.timestamp_before is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.timestamp <= self.timestamp_before)
        if self.is_junk is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.is_junk == self.is_junk)
        if self.person_ids is not None:
            query = query.filter(
                MigrationModelPersonSnapshot.person_id.in_(self.person_ids))
        if self.sort_by_list is not None:
            for sort_by in self.sort_by_list:
                if sort_by == RepositoryUtilDatabaseQueryPersonSnapshotSortByKey.TIMESTAMP_ASC:
                    query = query.order_by(
                        MigrationModelPersonSnapshot.timestamp.asc())
                elif sort_by == RepositoryUtilDatabaseQueryPersonSnapshotSortByKey.TIMESTAMP_DESC:
                    query = query.order_by(
                        MigrationModelPersonSnapshot.timestamp.desc())
        return query
