from dataclasses import dataclass
import uuid
from datetime import datetime
from dto.person.snapshot.meta_data import DtoPersonSnapshotMetaData

@dataclass
class DomainPersonSnapshotMetaData:
    """
    人物写真のメタデータを表すドメイン知識を集約する
    :param uuid.UUID id: 人物写真のID
    :param int camera_id: カメラID
    :param int view_id: ビューID
    :param datetime timestamp: 撮影時刻
    :param bool is_junk: ゴミかどうか
    :param uuid.UUID | None person_id: 人物ID
    """
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime
    is_junk: bool
    person_id: uuid.UUID | None

    def to_dto(self) -> DtoPersonSnapshotMetaData:
        return DtoPersonSnapshotMetaData(
            id=self.id,
            camera_id=self.camera_id,
            view_id=self.view_id,
            timestamp=self.timestamp,
            is_junk=self.is_junk,
            person_id=self.person_id,
        )
