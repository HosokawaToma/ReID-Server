"""
カメラフレーム用データベースクエリビルダ

camera_frames テーブルに対する条件・ソートを組み立てる。
"""
from dataclasses import dataclass
from datetime import datetime
import uuid
from sqlalchemy.orm import Query
from migration.models.camera_frames import MigrationModelCameraFrame
from enum import Enum


class RepositoryUtilDatabaseQueryCameraFrameSortByKey(str, Enum):
    """カメラフレームクエリのソートキー。"""
    TIMESTAMP_ASC = "timestamp_asc"
    TIMESTAMP_DESC = "timestamp_desc"

    def __str__(self) -> str:
        return self.value


@dataclass
class RepositoryUtilDatabaseQueryCameraFrame:
    """
    カメラフレームテーブル用のクエリ条件を保持するデータクラス。

    ID・カメラ・ビュー・時刻範囲・ソート順を保持し、SQLAlchemy の Query にフィルタと ORDER BY を適用した結果を返す。
    """
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    sort_by_list: list[RepositoryUtilDatabaseQueryCameraFrameSortByKey] | None = None

    def build(self, query: Query[MigrationModelCameraFrame]) -> Query[MigrationModelCameraFrame]:
        """
        保持する条件をベースクエリに適用し、フィルタ・ソートを付けたクエリを返す。条件が None の項目は適用しない。

        :param Query[MigrationModelCameraFrame] query: ベースとなるクエリ
        :return Query[MigrationModelCameraFrame]: 条件を適用したクエリ
        """
        if self.ids is not None:
            query = query.filter(MigrationModelCameraFrame.id.in_(self.ids))
        if self.camera_ids is not None:
            query = query.filter(
                MigrationModelCameraFrame.camera_id.in_(self.camera_ids))
        if self.view_ids is not None:
            query = query.filter(
                MigrationModelCameraFrame.view_id.in_(self.view_ids))
        if self.timestamp_after is not None:
            query = query.filter(
                MigrationModelCameraFrame.timestamp >= self.timestamp_after)
        if self.timestamp_before is not None:
            query = query.filter(
                MigrationModelCameraFrame.timestamp <= self.timestamp_before)
        if self.sort_by_list is not None:
            for sort_by in self.sort_by_list:
                if sort_by == RepositoryUtilDatabaseQueryCameraFrameSortByKey.TIMESTAMP_ASC:
                    query = query.order_by(
                        MigrationModelCameraFrame.timestamp.asc())
                elif sort_by == RepositoryUtilDatabaseQueryCameraFrameSortByKey.TIMESTAMP_DESC:
                    query = query.order_by(
                        MigrationModelCameraFrame.timestamp.desc())
        return query
