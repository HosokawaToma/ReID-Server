from dataclasses import dataclass
import uuid
from datetime import datetime
from sqlalchemy.orm import Query
from migration.models.person_snapshots import MigrationModelPersonSnapshot

from enum import Enum

class DatabaseQueryPersonSnapshotSortByKey(str, Enum):
    TIMESTAMP_ASC = "timestamp_asc"
    TIMESTAMP_DESC = "timestamp_desc"
    def __str__(self) -> str:
        return self.value

@dataclass
class DatabaseQueryPersonSnapshot:
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    is_junk: bool | None = None
    person_ids: list[uuid.UUID] | None = None
    sort_by_list: list[DatabaseQueryPersonSnapshotSortByKey] | None = None

    def build(self, query: Query[MigrationModelPersonSnapshot]) -> Query[MigrationModelPersonSnapshot]:
        """
        クエリをビルドする。
        :param Query[MigrationModelPersonSnapshot] query: クエリ
        :return Query[MigrationModelPersonSnapshot]: ビルドされたクエリ
        """
        if self.ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.id.in_(self.ids))
        if self.camera_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.camera_id.in_(self.camera_ids))
        if self.view_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.view_id.in_(self.view_ids))
        if self.timestamp_after is not None:
            query = query.filter(MigrationModelPersonSnapshot.timestamp >= self.timestamp_after)
        if self.timestamp_before is not None:
            query = query.filter(MigrationModelPersonSnapshot.timestamp <= self.timestamp_before)
        if self.is_junk is not None:
            query = query.filter(MigrationModelPersonSnapshot.is_junk == self.is_junk)
        if self.person_ids is not None:
            query = query.filter(MigrationModelPersonSnapshot.person_id.in_(self.person_ids))
        if self.sort_by_list is not None:
            for sort_by in self.sort_by_list:
                if sort_by == DatabaseQueryPersonSnapshotSortByKey.TIMESTAMP_ASC:
                    query = query.order_by(MigrationModelPersonSnapshot.timestamp.asc())
                elif sort_by == DatabaseQueryPersonSnapshotSortByKey.TIMESTAMP_DESC:
                    query = query.order_by(MigrationModelPersonSnapshot.timestamp.desc())
        return query
