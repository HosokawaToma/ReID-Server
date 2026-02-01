from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshotSortByKey
from environment import Environment
from applications import ApplicationBase
from dto.person.snapshot.detail import DtoPersonSnapshotDetail
from dto.person.snapshot.query import DtoPersonSnapshotQuery
from dto.pagination import DtoPagination
from dto.id import DtoId
from domain.pagination import DomainPagination
from domain.paging import DomainPaging
from domain.id import DomainId
from dto.date import DtoDate
from domain.date import DomainDate

class ApplicationPersonSnapshotSearch(ApplicationBase):
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
        search_limit: int,
    ):
        self.repository_person_snapshot = repository_person_snapshot
        self.search_limit = search_limit

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotSearch":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment=environment,
            ),
            search_limit=environment.search_limit,
        )

    def search(
        self,
        page: int,
        query: DtoPersonSnapshotQuery | None = None,
    ) -> list[DtoPersonSnapshotDetail]:
        """
        人物検出を検索する
        :param DtoPersonSnapshotQuery query: 人物検出検索条件
        :return list[DtoPersonSnapshotDetail]: 人物検出リスト
        :raises ApplicationPersonSnapshotSearchError: 人物検出検索に失敗した場合に発生するエラー
        """
        database_query = None
        if query is not None:
            database_query = RepositoryUtilDatabaseQueryPersonSnapshot(
                ids=query.ids,
                camera_ids=query.camera_ids,
                view_ids=query.view_ids,
                is_junk=query.is_junk,
                timestamp_after=query.timestamp_after,
                timestamp_before=query.timestamp_before,
                person_ids=query.person_ids,
                sort_by_list=[
                    RepositoryUtilDatabaseQueryPersonSnapshotSortByKey(sort_by.value)
                    for sort_by in query.sort_by_list
                ] if query.sort_by_list is not None else None,
            )
        detail_sequence = self.repository_person_snapshot.search_details(
            paging=DomainPaging(page=page, search_limit=self.search_limit),
            query=database_query,
        )
        return [DtoPersonSnapshotDetail(
            id=detail.id.id,
            camera_id=detail.location.camera_id,
            view_id=detail.location.view_id,
            timestamp=detail.timestamp.timestamp,
            is_junk=detail.person_id.is_junk,
            person_id=detail.person_id.id.id if detail.person_id.id is not None else None,
        ) for detail in detail_sequence]

    def search_paging(
        self,
        query: DtoPersonSnapshotQuery | None = None,
    ) -> DtoPagination:
        """
        人物検出結果の数を取得する
        :param DtoPersonSnapshotQuery query: 人物検出検索条件
        :return DtoPagination: 人物検出結果のページング
        :raises ApplicationPersonSnapshotSearchError: 人物検出結果の数取得に失敗した場合に発生するエラー
        """
        database_query = None
        if query is not None:
            database_query = RepositoryUtilDatabaseQueryPersonSnapshot(
                ids=query.ids,
                camera_ids=query.camera_ids,
                view_ids=query.view_ids,
                is_junk=query.is_junk,
                timestamp_after=query.timestamp_after,
                timestamp_before=query.timestamp_before,
                person_ids=query.person_ids,
            )
        total_items = self.repository_person_snapshot.count(query=database_query)
        pagination = DomainPagination.create(total_items=total_items, search_limit=self.search_limit)
        return DtoPagination(
            total_items=pagination.total_items,
            total_pages=pagination.total_pages,
        )

    def search_query_is_junk(self, date: DtoDate, page: int) -> list[DtoId]:
        """
        特定日のクエリデータを取得する
        :param DtoDate date: 日付
        :param int page: ページ番号
        :return list[DtoId]: クエリデータIDリスト
        :raises ApplicationPersonSnapshotSearchError: 人物検出検索に失敗した場合に発生するエラー
        """
        id_sequence = self.repository_person_snapshot.search_query_is_junk(
            date=DomainDate(year=date.year, month=date.month, day=date.day),
            paging=DomainPaging(page=page, search_limit=self.search_limit),
        )
        return [
            DtoId(id=id.id) for id in id_sequence
        ]

    def search_query_is_junk_paging(self, date: DtoDate) -> DtoPagination:
        """
        特定日のクエリデータの数を取得する
        :param DtoDate date: 日付
        :return DtoPagination: クエリデータのページング
        :raises ApplicationPersonSnapshotSearchError: クエリデータの数取得に失敗した場合に発生するエラー
        """
        total_items = self.repository_person_snapshot.count_query_is_junk(date=DomainDate(year=date.year, month=date.month, day=date.day))
        pagination = DomainPagination.create(total_items=total_items, search_limit=self.search_limit)
        return DtoPagination(
            total_items=pagination.total_items,
            total_pages=pagination.total_pages,
        )

    def search_query_is_not_junk(self, date: DtoDate, page: int) -> list[DtoId]:
        """
        特定日のクエリデータを取得する
        :param DtoDate date: 日付
        :param int page: ページ番号
        :return list[DtoId]: クエリデータIDリスト
        :raises ApplicationPersonSnapshotSearchError: 人物検出検索に失敗した場合に発生するエラー
        """
        id_sequence = self.repository_person_snapshot.search_query_is_not_junk(
            date=DomainDate(year=date.year, month=date.month, day=date.day),
            paging=DomainPaging(page=page, search_limit=self.search_limit),
        )
        return [
            DtoId(id=id.id) for id in id_sequence
        ]

    def search_query_is_not_junk_paging(self, date: DtoDate) -> DtoPagination:
        """
        特定日のクエリデータの数を取得する
        :param DtoDate date: 日付
        :return DtoPagination: クエリデータのページング
        :raises ApplicationPersonSnapshotSearchError: クエリデータの数取得に失敗した場合に発生するエラー
        """
        total_items = self.repository_person_snapshot.count_query_is_not_junk(date=DomainDate(year=date.year, month=date.month, day=date.day))
        pagination = DomainPagination.create(total_items=total_items, search_limit=self.search_limit)
        return DtoPagination(
            total_items=pagination.total_items,
            total_pages=pagination.total_pages,
        )

    def search_gallery_contains_junk(self, person_snapshot_id: DtoId) -> list[DtoId]:
        """
        特定日のギャラリーを取得する
        :param DtoId person_snapshot_id: 人物検出結果のID
        :return list[DtoId]: ギャラリーIDリスト
        :raises ApplicationPersonSnapshotSearchError: 人物検出検索に失敗した場合に発生するエラー
        """
        person_snapshot_feature = self.repository_person_snapshot.find_feature_by_id(
            person_snapshot_id=DomainId(id=person_snapshot_id.id),
        )
        id_sequence = self.repository_person_snapshot.search_gallery_contains_junk(
            person_snapshot_feature=person_snapshot_feature,
        )
        return [
            DtoId(id=id.id) for id in id_sequence
        ]

    def search_gallery_not_contains_junk(self, person_snapshot_id: DtoId) -> list[DtoId]:
        """
        ギャラリーデータを特徴量が最も近い順に取得する
        ※ゴミデータは除外する
        :param DtoId person_snapshot_id: 人物検出結果のID
        :return list[DtoId]: ギャラリーIDリスト
        :raises ApplicationPersonSnapshotSearchError: 人物検出検索に失敗した場合に発生するエラー
        """
        person_snapshot_feature = self.repository_person_snapshot.find_feature_by_id(
            person_snapshot_id=DomainId(id=person_snapshot_id.id),
        )
        id_sequence = self.repository_person_snapshot.search_gallery_not_contains_junk(
            person_snapshot_feature=person_snapshot_feature,
        )
        return [
            DtoId(id=id.id) for id in id_sequence
        ]
