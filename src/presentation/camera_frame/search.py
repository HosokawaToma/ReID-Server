"""
カメラフレーム検索のプレゼンテーション層

POST /frame/search/{page} でページ番号と検索条件（ID・カメラ・ビュー・時刻範囲・ソート）を受け取り、
カメラフレーム一覧と総件数・ページング情報を JSON で返す API を提供する。認証済み管理クライアントのみ利用可能。成功時は 200。
"""
from applications.camera_frame.search import ApplicationCameraFrameSearch
from presentation.utils.base import PresentationUtilBase
from presentation.utils.factory import get_application
from logger import Logger
from presentation.utils.request import PresentationUtilRequestBody
from dto.camera_frame.query import DtoCameraFrameQuery, DtoCameraFrameQuerySortByKey
from dataclasses import dataclass
from datetime import datetime
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
import uuid
from enum import Enum
from presentation.utils.type import PresentationUtilPathInt


class PresentationCameraFrameSearchSortByKey(str, Enum):
    """カメラフレーム検索のソートキー。"""
    TIMESTAMP_ASC = "timestamp_asc"
    TIMESTAMP_DESC = "timestamp_desc"


@dataclass
class PresentationCameraFrameSearchRequestBody(PresentationUtilRequestBody):
    """
    カメラフレーム検索 API のリクエストボディを保持する DTO。

    ID 一覧（ids）、カメラ ID 一覧（camera_ids）、ビュー ID 一覧（view_ids）、撮影時刻範囲（timestamp_after, timestamp_before）、ソート順（sort_by_list）を任意で指定する。すべて省略可能。
    """
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    sort_by_list: list[PresentationCameraFrameSearchSortByKey] | None = None


class PresentationCameraFrameSearch(PresentationUtilBase):
    """
    カメラフレーム検索の API エンドポイントを担当するプレゼンテーション。

    POST /frame/search/{page} でページ番号（パス）とボディの検索条件を送信し、該当するカメラフレームの一覧と総件数・ページング情報を取得する。成功時は 200 と camera_frames, pagination を返す。Bearer トークン必須。
    """
    router_path = "/frame/search/{page}"
    methods = ["POST"]
    tags = ["Camera Frame"]
    summary = "Search camera frames"
    description = "Search camera frames"
    responses = {
        200: {
            "description": "Frames",
        },
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationCameraFrameSearch":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationCameraFrameSearch: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_camera_frame_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        page: PresentationUtilPathInt,
        body: PresentationCameraFrameSearchRequestBody | None = None,
        application: ApplicationCameraFrameSearch = get_application(
            ApplicationCameraFrameSearch),
    ) -> PresentationUtilJSONResponse:
        """
        リクエストの条件とページ番号でカメラフレームを検索し、一覧とページング情報を JSON で返す。

        ボディが None の場合はクエリを None にし、全件対象のうち指定ページを取得する。アプリケーション層で search と search_paging を呼び、camera_frames 配列と pagination をレスポンスに含める。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationUtilPathInt page: ページ番号（パス: /frame/search/{page}）
        :param PresentationCameraFrameSearchRequestBody body: 検索条件（None の場合は全件）
        :param ApplicationCameraFrameSearch application: カメラフレーム検索アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と camera_frames, pagination を含む JSON
        """
        query = None
        if body is not None:
            query = DtoCameraFrameQuery(
                ids=body.ids,
                camera_ids=body.camera_ids,
                view_ids=body.view_ids,
                timestamp_after=body.timestamp_after,
                timestamp_before=body.timestamp_before,
                sort_by_list=[
                    DtoCameraFrameQuerySortByKey(sort_by.value)
                    for sort_by in body.sort_by_list
                ] if body.sort_by_list is not None else None,
            )
        camera_frames = application.search(page=page, query=query)
        paging = application.search_paging(query=query)
        return PresentationUtilJSONResponse(status=200, content={
            "camera_frames": [
                {
                    "id": str(camera_frame.id),
                    "camera_id": camera_frame.camera_id,
                    "view_id": camera_frame.view_id,
                    "timestamp": camera_frame.timestamp.isoformat(),
                } for camera_frame in camera_frames
            ],
            "pagination": {
                "total_items": paging.total_items,
                "total_pages": paging.total_pages,
            },
        })
