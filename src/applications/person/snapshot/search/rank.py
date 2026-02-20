"""
人物検出ランキング検索アプリケーション

指定した人物検出結果をクエリに、別カメラ・同日の類似度順ランキングを取得する。
"""
from applications import ApplicationBase
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from dto.person.snapshot.detail import DtoPersonSnapshotDetail
from domain.id import DomainId
from dto.id import DtoId
from dto.pagination import DtoPagination
from domain.pagination import DomainPagination
from domain.paging import DomainPaging


class ApplicationPersonSnapshotSearchRank(ApplicationBase):
    """
    人物検出の「ランキング」検索を担当するアプリケーション。

    指定した人物検出結果をクエリに、別カメラ・同日のフレームから類似度順の詳細リストとページング情報を返す。
    """

    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot, search_limit: int):
        """
        アプリケーションを初期化する。

        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        :param int search_limit: 1ページあたりの件数
        """
        self.repository_person_snapshot = repository_person_snapshot
        self.search_limit = search_limit

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotSearchRank":
        """
        環境からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return ApplicationPersonSnapshotSearchRank: アプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment=environment),
            search_limit=environment.search_limit,
        )

    def search(self, person_snapshot_id: DtoId, page: int) -> list[DtoPersonSnapshotDetail]:
        """
        指定した人物検出結果をクエリに、別カメラ・同日の類似度順（ランキング）で人物検出詳細のリストを返す。

        :param DtoId person_snapshot_id: クエリとする人物検出結果のID
        :param int page: ページ番号（1 始まり）
        :return list[DtoPersonSnapshotDetail]: ランキング順の人物検出詳細リスト
        :raises ApplicationPersonSnapshotSearchRankError: 検索に失敗した場合
        """
        person_snapshot_feature = self.repository_person_snapshot.find_feature_by_id(
            DomainId(id=person_snapshot_id.id))
        person_snapshot_details = self.repository_person_snapshot.search_details_by_ranking(
            person_snapshot=person_snapshot_feature,
            paging=DomainPaging(page=page, search_limit=self.search_limit),
        )
        return [DtoPersonSnapshotDetail(
            id=person_snapshot_detail.id.id,
            camera_id=person_snapshot_detail.location.camera_id,
            view_id=person_snapshot_detail.location.view_id,
            timestamp=person_snapshot_detail.timestamp.timestamp,
            is_junk=person_snapshot_detail.person_id.is_junk,
            person_id=person_snapshot_detail.person_id.id.id if person_snapshot_detail.person_id.id is not None else None,
        ) for person_snapshot_detail in person_snapshot_details]

    def search_paging(self, person_snapshot_id: DtoId) -> DtoPagination:
        """
        指定した人物検出結果のランキング検索結果の総件数と総ページ数を返す。

        :param DtoId person_snapshot_id: クエリとする人物検出結果のID
        :return DtoPagination: 総件数と総ページ数
        :raises ApplicationPersonSnapshotSearchRankError: 件数取得に失敗した場合
        """
        person_snapshot = self.repository_person_snapshot.find_detail_by_id(
            DomainId(id=person_snapshot_id.id))
        total_items = self.repository_person_snapshot.count_by_ranking(
            person_snapshot=person_snapshot)
        pagination = DomainPagination.create(
            total_items=total_items, search_limit=self.search_limit)
        return DtoPagination(total_items=pagination.total_items, total_pages=pagination.total_pages)
