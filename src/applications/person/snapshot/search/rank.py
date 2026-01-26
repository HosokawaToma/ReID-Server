from applications import ApplicationBase
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from dto.person.snapshot.detail import DtoPersonSnapshotDetail
from domain.id import DomainId
from dto.id import DtoId
from error import ValidationError
from typing import ClassVar


class ApplicationPersonSnapshotSearchRank(ApplicationBase):
    MIN_LIMIT: ClassVar[int] = 1
    MAX_LIMIT: ClassVar[int] = 1000
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotSearchRank":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment=environment),
        )

    def search(self, person_snapshot_id: DtoId, limit: int | None = None) -> list[DtoPersonSnapshotDetail]:
        """
        人物検出結果のランキングを検索する
        :param DtoId person_snapshot_id: 人物検出結果のID
        :param int limit: 取得する人物検出結果の数
        :return list[DtoPersonSnapshotDetail]: 人物検出結果のランキングリスト
        :raises ApplicationPersonSnapshotSearchRankError: 人物検出結果のランキング検索に失敗した場合に発生するエラー
        """
        if limit is not None:
            self._validate_limit(limit)
        person_snapshot_feature = self.repository_person_snapshot.find_feature_by_id(DomainId(id=person_snapshot_id.id))
        person_snapshot_details = self.repository_person_snapshot.find_details_by_ranking(person_snapshot_feature, limit if limit is not None else self.MIN_LIMIT)
        return [DtoPersonSnapshotDetail(
            id=person_snapshot_detail.id.id,
            camera_id=person_snapshot_detail.location.camera_id,
            view_id=person_snapshot_detail.location.view_id,
            timestamp=person_snapshot_detail.timestamp.timestamp,
            is_junk=person_snapshot_detail.person_id.is_junk,
            person_id=person_snapshot_detail.person_id.id.id if person_snapshot_detail.person_id.id is not None else None,
        ) for person_snapshot_detail in person_snapshot_details]

    def _validate_limit(self, limit: int) -> None:
        if limit < self.MIN_LIMIT:
            raise ValidationError("limitは1以上である必要があります")
        if limit > self.MAX_LIMIT:
            raise ValidationError("limitは1000以下である必要があります")
