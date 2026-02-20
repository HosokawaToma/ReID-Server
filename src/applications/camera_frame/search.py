"""
カメラフレーム検索アプリケーション

ページとクエリ条件でカメラフレームを検索し、DTOとページングを返す。
"""
from repositories.camera_frame import RepositoryCameraFrame
from repositories.utils.database.query.camera_frame import RepositoryUtilDatabaseQueryCameraFrame
from repositories.utils.database.query.camera_frame import RepositoryUtilDatabaseQueryCameraFrameSortByKey
from dto.camera_frame import DtoCameraFrame
from dto.camera_frame.query import DtoCameraFrameQuery
from environment import Environment
from applications import ApplicationBase
from domain.paging import DomainPaging
from dto.pagination import DtoPagination
from domain.pagination import DomainPagination


class ApplicationCameraFrameSearch(ApplicationBase):
    """
    カメラフレーム検索を担当するアプリケーション。

    ページ番号と検索条件（ID・カメラ・ビュー・時刻範囲・ソート）を受け取り、該当するカメラフレームのリストと総件数・総ページ数を返す。
    """

    def __init__(self, repository_camera_frame: RepositoryCameraFrame, search_limit: int):
        """
        カメラフレームリポジトリと 1 ページあたり件数を設定する。

        :param RepositoryCameraFrame repository_camera_frame: カメラフレームリポジトリ
        :param int search_limit: 1 ページあたりの最大件数
        """
        self.repository_camera_frame = repository_camera_frame
        self.search_limit = search_limit

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationCameraFrameSearch":
        """
        環境からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return ApplicationCameraFrameSearch: アプリケーションインスタンス
        """
        return cls(
            repository_camera_frame=RepositoryCameraFrame.create(environment),
            search_limit=environment.search_limit,
        )

    def search(
        self,
        page: int,
        query: DtoCameraFrameQuery | None = None,
    ) -> list[DtoCameraFrame]:
        """
        ページ番号と検索条件に応じてカメラフレームの一覧を返す。

        条件が None の場合は全件対象。ページングは 1 始まりで、1 ページあたりの件数は初期化時に指定した値を使用する。検索失敗時は ApplicationCameraFrameSearchError。

        :param int page: ページ番号（1 以上）
        :param DtoCameraFrameQuery query: 検索条件（None の場合は条件なし）
        :return list[DtoCameraFrame]: 該当するカメラフレームのリスト
        :raises ApplicationCameraFrameSearchError: 検索に失敗した場合
        """
        database_query = None
        if query is not None:
            database_query = RepositoryUtilDatabaseQueryCameraFrame(
                ids=query.ids,
                camera_ids=query.camera_ids,
                view_ids=query.view_ids,
                timestamp_after=query.timestamp_after,
                timestamp_before=query.timestamp_before,
                sort_by_list=[
                    RepositoryUtilDatabaseQueryCameraFrameSortByKey(
                        sort_by.value)
                    for sort_by in query.sort_by_list
                ] if query.sort_by_list is not None else None,
            )
        camera_frames = self.repository_camera_frame.search(
            paging=DomainPaging(page=page, search_limit=self.search_limit),
            query=database_query,
        )
        return [DtoCameraFrame(
            id=camera_frame.id.id,
            camera_id=camera_frame.location.camera_id,
            view_id=camera_frame.location.view_id,
            timestamp=camera_frame.timestamp.timestamp,
        ) for camera_frame in camera_frames]

    def search_paging(
        self,
        query: DtoCameraFrameQuery | None = None,
    ) -> DtoPagination:
        """
        検索条件に一致するカメラフレームの総件数と、1 ページあたり件数から求めた総ページ数を返す。

        条件が None の場合は全件数。検索失敗時は ApplicationCameraFrameSearchError。

        :param DtoCameraFrameQuery query: 検索条件（None の場合は条件なし）
        :return DtoPagination: 総件数と総ページ数
        :raises ApplicationCameraFrameSearchError: 件数取得に失敗した場合
        """
        database_query = None
        if query is not None:
            database_query = RepositoryUtilDatabaseQueryCameraFrame(
                ids=query.ids,
                camera_ids=query.camera_ids,
                view_ids=query.view_ids,
                timestamp_after=query.timestamp_after,
                timestamp_before=query.timestamp_before,
            )
        total_items = self.repository_camera_frame.search_count(
            query=database_query)
        pagination = DomainPagination.create(
            total_items=total_items, search_limit=self.search_limit)
        return DtoPagination(
            total_items=pagination.total_items,
            total_pages=pagination.total_pages,
        )
