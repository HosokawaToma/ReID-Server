from applications import ApplicationBase
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from domain.paging import DomainPaging
from dto.person.snapshot.detail import DtoPersonSnapshotDetail
from dto.id import DtoId
from domain.id import DomainId

class ApplicationPersonSnapshotSearchNearest(ApplicationBase):
    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot, search_limit: int):
        self.repository_person_snapshot = repository_person_snapshot
        self.search_limit = search_limit

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotSearchNearest":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
            search_limit=environment.search_limit,
        )

    def search(self, person_snapshot_id: DtoId, page: int) -> list[DtoPersonSnapshotDetail]:
        """
        同じ日付で特徴量が最も近い順に人物検出結果を検索する
        :param DtoId person_snapshot_id: 人物検出結果のID
        :param int page: ページ番号
        :return list[DtoPersonSnapshotDetail]: 特徴量が最も近い順に検索した人物検出結果リスト
        """
        person_snapshot = self.repository_person_snapshot.find_feature_by_id(DomainId(id=person_snapshot_id.id))
        person_snapshot_details = self.repository_person_snapshot.search_details_by_nearest(person_snapshot=person_snapshot, paging=DomainPaging(page=page, search_limit=self.search_limit))
        return [DtoPersonSnapshotDetail(
            id=person_snapshot_detail.id.id,
            camera_id=person_snapshot_detail.location.camera_id,
            view_id=person_snapshot_detail.location.view_id,
            timestamp=person_snapshot_detail.timestamp.timestamp,
            is_junk=person_snapshot_detail.person_id.is_junk,
            person_id=person_snapshot_detail.person_id.id.id if person_snapshot_detail.person_id.id is not None else None,
        ) for person_snapshot_detail in person_snapshot_details]
