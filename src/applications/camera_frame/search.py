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
    カメラフレームを検索するアプリケーションクラス。
    """

    def __init__(self, repository_camera_frame: RepositoryCameraFrame, search_limit: int):
        """
        アプリケーションを初期化する。

        :param RepositoryCameraFrame repository_camera_frame: カメラフレームリポジトリ
        :param int search_limit: 1ページあたりの件数
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
        カメラフレームを検索する
        :param int page: ページ番号
        :param DtoCameraFrameQuery query: カメラフレーム検索条件
        :return list[DtoCameraFrame]: カメラフレームリスト
        :raises ApplicationCameraFrameSearchError: カメラフレーム検索に失敗した場合に発生するエラー
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
        カメラフレームの数を取得する
        :param DtoCameraFrameQuery query: カメラフレーム検索条件
        :return DtoPagination: カメラフレームのページング
        :raises ApplicationCameraFrameSearchError: カメラフレームの数取得に失敗した場合に発生するエラー
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
