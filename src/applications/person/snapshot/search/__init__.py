"""
人物検出検索アプリケーション

ページとクエリ条件で人物検出結果を検索し、DTOとページングを返す。
"""
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
from error import ValidationError


class ApplicationPersonSnapshotSearch(ApplicationBase):
    """
    人物検出結果の検索を担当するアプリケーション。

    ページ番号とクエリ条件（ID・カメラ・ビュー・ゴミフラグ・時刻範囲・人物ID・ソート）に応じて、詳細リスト・総件数・総ページ数・ギャラリーID などを返す。
    """

    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
        search_limit: int,
    ):
        """
        アプリケーションを初期化する。

        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        :param int search_limit: 1ページあたりの件数
        """
        self.repository_person_snapshot = repository_person_snapshot
        self.search_limit = search_limit

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotSearch":
        """
        環境からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return ApplicationPersonSnapshotSearch: アプリケーションインスタンス
        """
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
        指定ページ・クエリ条件で人物検出結果の詳細リストを返す。条件が None の場合は全件を対象とする。

        :param int page: ページ番号（1 始まり）
        :param DtoPersonSnapshotQuery | None query: 検索条件（省略時は全件）
        :return list[DtoPersonSnapshotDetail]: 人物検出詳細のリスト
        :raises ApplicationPersonSnapshotSearchError: 検索処理に失敗した場合
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
                    RepositoryUtilDatabaseQueryPersonSnapshotSortByKey(
                        sort_by.value)
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
        クエリ条件に合致する人物検出結果の総件数と総ページ数を返す。条件が None の場合は全件を対象とする。

        :param DtoPersonSnapshotQuery | None query: 検索条件（省略時は全件）
        :return DtoPagination: 総件数と総ページ数
        :raises ApplicationPersonSnapshotSearchError: 件数取得に失敗した場合
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
        total_items = self.repository_person_snapshot.count(
            query=database_query)
        pagination = DomainPagination.create(
            total_items=total_items, search_limit=self.search_limit)
        return DtoPagination(
            total_items=pagination.total_items,
            total_pages=pagination.total_pages,
        )

    def search_query_is_junk(self, date: DtoDate, page: int) -> list[DtoId]:
        """
        指定日に「ゴミ」とマークされた人物検出結果のIDを、ページングで返す。

        :param DtoDate date: 対象日
        :param int page: ページ番号（1 始まり）
        :return list[DtoId]: 人物検出結果IDのリスト
        :raises ApplicationPersonSnapshotSearchError: 検索に失敗した場合
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
        指定日に「ゴミ」とマークされた人物検出結果の総件数と総ページ数を返す。

        :param DtoDate date: 対象日
        :return DtoPagination: 総件数と総ページ数
        :raises ApplicationPersonSnapshotSearchError: 件数取得に失敗した場合
        """
        total_items = self.repository_person_snapshot.count_query_is_junk(
            date=DomainDate(year=date.year, month=date.month, day=date.day))
        pagination = DomainPagination.create(
            total_items=total_items, search_limit=self.search_limit)
        return DtoPagination(
            total_items=pagination.total_items,
            total_pages=pagination.total_pages,
        )

    def search_query_is_not_junk(self, date: DtoDate, page: int) -> list[DtoId]:
        """
        指定日に「ゴミでない」とマークされた人物検出結果のIDを、ページングで返す。

        :param DtoDate date: 対象日
        :param int page: ページ番号（1 始まり）
        :return list[DtoId]: 人物検出結果IDのリスト
        :raises ApplicationPersonSnapshotSearchError: 検索に失敗した場合
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
        指定日に「ゴミでない」とマークされた人物検出結果の総件数と総ページ数を返す。

        :param DtoDate date: 対象日
        :return DtoPagination: 総件数と総ページ数
        :raises ApplicationPersonSnapshotSearchError: 件数取得に失敗した場合
        """
        total_items = self.repository_person_snapshot.count_query_is_not_junk(
            date=DomainDate(year=date.year, month=date.month, day=date.day))
        pagination = DomainPagination.create(
            total_items=total_items, search_limit=self.search_limit)
        return DtoPagination(
            total_items=pagination.total_items,
            total_pages=pagination.total_pages,
        )

    def search_gallery_contains_junk(self, person_snapshot_id: DtoId) -> list[DtoId]:
        """
        指定した人物検出結果をクエリとして、正解データを含むギャラリー（類似人物検出結果のIDリスト）を返す。正解が無い場合は ValidationError。

        :param DtoId person_snapshot_id: クエリとする人物検出結果のID
        :return list[DtoId]: ギャラリーに含まれる人物検出結果IDのリスト
        :raises ApplicationPersonSnapshotSearchError: 検索に失敗した場合
        :raises ValidationError: 正解データが無い場合
        """
        self._validate_search_gallery_contains_junk(
            person_snapshot_id=person_snapshot_id)
        person_snapshot_feature = self.repository_person_snapshot.find_feature_by_id(
            person_snapshot_id=DomainId(id=person_snapshot_id.id),
        )
        id_sequence = self.repository_person_snapshot.search_gallery_contains_junk(
            person_snapshot_feature=person_snapshot_feature,
        )
        return [
            DtoId(id=id.id) for id in id_sequence
        ]

    def _validate_search_gallery_contains_junk(self, person_snapshot_id: DtoId) -> None:
        """
        指定した人物検出結果に正解ラベルが存在し、ギャラリーに正解が含まれることを検証する。満たさない場合は ValidationError を送出する。

        :param DtoId person_snapshot_id: 対象の人物検出結果のID
        :raises ValidationError: 正解が無い、またはギャラリーに正解が含まれない場合
        """
        person_snapshot_detail_answer = self.repository_person_snapshot.find_detail_answer_by_id(
            person_snapshot_id=DomainId(id=person_snapshot_id.id),
        )
        if not self.repository_person_snapshot.exists_gallery_contains_junk(
            person_snapshot_detail_answer=person_snapshot_detail_answer,
        ):
            raise ValidationError("ギャラリーデータに正解データが含まれていません")

    def search_gallery_not_contains_junk(self, person_snapshot_id: DtoId) -> list[DtoId]:
        """
        指定した人物検出結果をクエリとして、ゴミを除外したギャラリー（特徴量が近い順の人物検出結果IDリスト）を返す。正解が無い場合は ValidationError。

        :param DtoId person_snapshot_id: クエリとする人物検出結果のID
        :return list[DtoId]: ギャラリーに含まれる人物検出結果IDのリスト
        :raises ApplicationPersonSnapshotSearchError: 検索に失敗した場合
        :raises ValidationError: 正解データが無い場合
        """
        self._validate_search_gallery_not_contains_junk(
            person_snapshot_id=person_snapshot_id)
        person_snapshot_feature = self.repository_person_snapshot.find_feature_by_id(
            person_snapshot_id=DomainId(id=person_snapshot_id.id),
        )
        id_sequence = self.repository_person_snapshot.search_gallery_not_contains_junk(
            person_snapshot_feature=person_snapshot_feature,
        )
        return [
            DtoId(id=id.id) for id in id_sequence
        ]

    def _validate_search_gallery_not_contains_junk(self, person_snapshot_id: DtoId) -> None:
        """
        指定した人物検出結果に正解ラベルが存在し、ギャラリー（ゴミ除外）に正解が含まれることを検証する。満たさない場合は ValidationError を送出する。

        :param DtoId person_snapshot_id: 対象の人物検出結果のID
        :raises ValidationError: 正解が無い、またはギャラリーに正解が含まれない場合
        """
        person_snapshot_detail_answer = self.repository_person_snapshot.find_detail_answer_by_id(
            person_snapshot_id=DomainId(id=person_snapshot_id.id),
        )
        if not self.repository_person_snapshot.exists_gallery_not_contains_junk(
            person_snapshot_detail_answer=person_snapshot_detail_answer,
        ):
            raise ValidationError("ギャラリーデータに正解データが含まれていません")
