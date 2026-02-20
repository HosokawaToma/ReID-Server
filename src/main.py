"""
アプリケーションエントリポイント

FastAPI アプリを組み立て、管理認証・人物検出・カメラフレーム・ReID 評価等のルートを登録し、指定ホスト・ポートで HTTP サーバを起動する。
"""
import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from environment import Environment
from presentation.admin.auth.login import PresentationAdminAuthLogin
from presentation.admin.auth.token_refresh import PresentationAdminAuthTokenRefresh
from presentation.person.snapshot.create import PresentationPersonSnapshotCreate
from presentation.person.snapshot.refresh import PresentationPersonSnapshotRefresh
from presentation.person.snapshot.refresh.detect_junk import PresentationPersonSnapshotRefreshDetectJunk
from presentation.person.snapshot.search import PresentationPersonSnapshotSearch
from presentation.person.flow.search import PresentationPersonFlowSearch
from presentation.person.flow.weight.search import PresentationPersonFlowWeightSearch
from presentation.person.snapshot.image.search import PresentationPersonSnapshotImageSearch
from presentation.camera_frame.search import PresentationCameraFrameSearch
from presentation.camera_frame.image.search import PresentationCameraFrameImageSearch
from presentation.person.snapshot.answer.search import PresentationPersonSnapshotAnswerSearch
from presentation.person.snapshot.answer.assign import PresentationPersonSnapshotAnswerAssign
from presentation.person.snapshot.answer.delete import PresentationPersonSnapshotAnswerDelete
from presentation.person.snapshot.search.rank import PresentationPersonSnapshotSearchRank
from presentation.person.snapshot.search.nearest import PresentationPersonSnapshotSearchNearest
from presentation.person.snapshot.search.query.is_not_junk import PresentationPersonSnapshotSearchQueryIsNotJunk
from presentation.person.snapshot.search.query.is_junk import PresentationPersonSnapshotSearchQueryIsJunk
from presentation.person.snapshot.search.gallery.contains_junk import PresentationPersonSnapshotSearchGalleryContainsJunk
from presentation.person.snapshot.search.gallery.not_contains_junk import PresentationPersonSnapshotSearchGalleryNotContainsJunk
from presentation.person.snapshot.refresh.feature_extract import PresentationPersonSnapshotRefreshFeatureExtract
from presentation.reid.evaluation import PresentationReidEvaluation


class ServerApp:
    """
    HTTP サーバのエントリポイントを担当するクラス。

    認証・人物スナップショット・カメラフレーム・人物フロー・ReID 評価など各エンドポイントを 1 ルートずつ登録し、uvicorn で指定ホスト・ポートに HTTP サーバを起動する。
    """

    def __init__(
        self,
        app_host: str,
        app_port: int,
        fastapi_app: fastapi.FastAPI,
        admin_auth_login: PresentationAdminAuthLogin,
        admin_auth_token_refresh: PresentationAdminAuthTokenRefresh,
        person_snapshot_create: PresentationPersonSnapshotCreate,
        person_snapshot_refresh: PresentationPersonSnapshotRefresh,
        person_snapshot_refresh_detect_junk: PresentationPersonSnapshotRefreshDetectJunk,
        person_snapshot_search: PresentationPersonSnapshotSearch,
        person_flow_search: PresentationPersonFlowSearch,
        person_flow_weight_search: PresentationPersonFlowWeightSearch,
        person_snapshot_image_search: PresentationPersonSnapshotImageSearch,
        person_snapshot_answer_search: PresentationPersonSnapshotAnswerSearch,
        person_snapshot_answer_assign: PresentationPersonSnapshotAnswerAssign,
        person_snapshot_answer_delete: PresentationPersonSnapshotAnswerDelete,
        person_snapshot_search_rank: PresentationPersonSnapshotSearchRank,
        person_snapshot_search_nearest: PresentationPersonSnapshotSearchNearest,
        camera_frame_search: PresentationCameraFrameSearch,
        camera_frame_image_search: PresentationCameraFrameImageSearch,
        person_snapshot_refresh_feature_extract: PresentationPersonSnapshotRefreshFeatureExtract,
        person_snapshot_search_query_is_not_junk: PresentationPersonSnapshotSearchQueryIsNotJunk,
        person_snapshot_search_query_is_junk: PresentationPersonSnapshotSearchQueryIsJunk,
        person_snapshot_search_gallery_contains_junk: PresentationPersonSnapshotSearchGalleryContainsJunk,
        person_snapshot_search_gallery_not_contains_junk: PresentationPersonSnapshotSearchGalleryNotContainsJunk,
        reid_evaluation: PresentationReidEvaluation,
    ):
        """
        サーバアプリを初期化する。

        :param str app_host: バインドするホスト
        :param int app_port: バインドするポート
        :param fastapi.FastAPI fastapi_app: FastAPIアプリケーション
        :param PresentationAdminAuthLogin admin_auth_login: 管理認証ログイン
        :param PresentationAdminAuthTokenRefresh admin_auth_token_refresh: トークンリフレッシュ
        :param PresentationPersonSnapshotCreate person_snapshot_create: 人物検出作成
        :param PresentationPersonSnapshotRefresh person_snapshot_refresh: 人物検出更新
        :param PresentationPersonSnapshotRefreshDetectJunk person_snapshot_refresh_detect_junk: ジャンク判定
        :param PresentationPersonSnapshotSearch person_snapshot_search: 人物検出検索
        :param PresentationPersonFlowSearch person_flow_search: 人物フロー検索
        :param PresentationPersonFlowWeightSearch person_flow_weight_search: フロー重み検索
        :param PresentationPersonSnapshotImageSearch person_snapshot_image_search: 人物検出画像検索
        :param PresentationPersonSnapshotAnswerSearch person_snapshot_answer_search: 正解検索
        :param PresentationPersonSnapshotAnswerAssign person_snapshot_answer_assign: 正解割当
        :param PresentationPersonSnapshotAnswerDelete person_snapshot_answer_delete: 正解削除
        :param PresentationPersonSnapshotSearchRank person_snapshot_search_rank: ランク検索
        :param PresentationPersonSnapshotSearchNearest person_snapshot_search_nearest: 最近傍検索
        :param PresentationCameraFrameSearch camera_frame_search: カメラフレーム検索
        :param PresentationCameraFrameImageSearch camera_frame_image_search: カメラフレーム画像検索
        :param PresentationPersonSnapshotRefreshFeatureExtract person_snapshot_refresh_feature_extract: 特徴量抽出
        :param PresentationPersonSnapshotSearchQueryIsNotJunk person_snapshot_search_query_is_not_junk: クエリ（非ジャンク）
        :param PresentationPersonSnapshotSearchQueryIsJunk person_snapshot_search_query_is_junk: クエリ（ジャンク）
        :param PresentationPersonSnapshotSearchGalleryContainsJunk person_snapshot_search_gallery_contains_junk: ギャラリー（ジャンク含む）
        :param PresentationPersonSnapshotSearchGalleryNotContainsJunk person_snapshot_search_gallery_not_contains_junk: ギャラリー（ジャンク除く）
        :param PresentationReidEvaluation reid_evaluation: 再識別評価
        """
        self.app_host = app_host
        self.app_port = app_port
        self.fastapi_app = fastapi_app
        self.admin_auth_login = admin_auth_login
        self.admin_auth_token_refresh = admin_auth_token_refresh
        self.person_snapshot_create = person_snapshot_create
        self.person_snapshot_refresh = person_snapshot_refresh
        self.person_snapshot_refresh_detect_junk = person_snapshot_refresh_detect_junk
        self.person_snapshot_search = person_snapshot_search
        self.person_flow_search = person_flow_search
        self.person_flow_weight_search = person_flow_weight_search
        self.person_snapshot_image_search = person_snapshot_image_search
        self.person_snapshot_answer_search = person_snapshot_answer_search
        self.person_snapshot_answer_assign = person_snapshot_answer_assign
        self.person_snapshot_answer_delete = person_snapshot_answer_delete
        self.person_snapshot_search_rank = person_snapshot_search_rank
        self.person_snapshot_search_nearest = person_snapshot_search_nearest
        self.camera_frame_search = camera_frame_search
        self.camera_frame_image_search = camera_frame_image_search
        self.person_snapshot_refresh_feature_extract = person_snapshot_refresh_feature_extract
        self.person_snapshot_search_query_is_not_junk = person_snapshot_search_query_is_not_junk
        self.person_snapshot_search_query_is_junk = person_snapshot_search_query_is_junk
        self.person_snapshot_search_gallery_contains_junk = person_snapshot_search_gallery_contains_junk
        self.person_snapshot_search_gallery_not_contains_junk = person_snapshot_search_gallery_not_contains_junk
        self.reid_evaluation = reid_evaluation

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ServerApp":
        """
        環境からサーバアプリインスタンスを生成する。

        :param Environment environment: 環境設定
        :return ServerApp: サーバアプリインスタンス
        """
        return cls(
            app_host=environment.app_host,
            app_port=environment.app_port,
            fastapi_app=fastapi.FastAPI(
                servers=[{"url": "/api/v1"}],
                root_path="/api/v1"
            ),
            admin_auth_login=PresentationAdminAuthLogin.create(),
            admin_auth_token_refresh=PresentationAdminAuthTokenRefresh.create(),
            person_snapshot_create=PresentationPersonSnapshotCreate.create(),
            person_snapshot_refresh=PresentationPersonSnapshotRefresh.create(),
            person_snapshot_refresh_detect_junk=PresentationPersonSnapshotRefreshDetectJunk.create(),
            person_snapshot_search=PresentationPersonSnapshotSearch.create(),
            person_flow_search=PresentationPersonFlowSearch.create(),
            person_flow_weight_search=PresentationPersonFlowWeightSearch.create(),
            person_snapshot_image_search=PresentationPersonSnapshotImageSearch.create(),
            person_snapshot_answer_search=PresentationPersonSnapshotAnswerSearch.create(),
            person_snapshot_answer_assign=PresentationPersonSnapshotAnswerAssign.create(),
            person_snapshot_answer_delete=PresentationPersonSnapshotAnswerDelete.create(),
            person_snapshot_search_rank=PresentationPersonSnapshotSearchRank.create(),
            person_snapshot_search_nearest=PresentationPersonSnapshotSearchNearest.create(),
            camera_frame_search=PresentationCameraFrameSearch.create(),
            camera_frame_image_search=PresentationCameraFrameImageSearch.create(),
            person_snapshot_refresh_feature_extract=PresentationPersonSnapshotRefreshFeatureExtract.create(),
            person_snapshot_search_query_is_not_junk=PresentationPersonSnapshotSearchQueryIsNotJunk.create(),
            person_snapshot_search_query_is_junk=PresentationPersonSnapshotSearchQueryIsJunk.create(),
            person_snapshot_search_gallery_contains_junk=PresentationPersonSnapshotSearchGalleryContainsJunk.create(),
            person_snapshot_search_gallery_not_contains_junk=PresentationPersonSnapshotSearchGalleryNotContainsJunk.create(),
            reid_evaluation=PresentationReidEvaluation.create(),
        )

    def run(self) -> None:
        """
        CORS を許可するミドルウェアを追加し、全エンドポイントをルート登録したのち、指定ホスト・ポートで HTTP サーバを起動する。ブロッキングで動作する。
        """
        self.fastapi_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.admin_auth_login.setup(self.fastapi_app)
        self.admin_auth_token_refresh.setup(self.fastapi_app)
        self.person_snapshot_create.setup(self.fastapi_app)
        self.person_snapshot_refresh.setup(self.fastapi_app)
        self.person_snapshot_refresh_detect_junk.setup(self.fastapi_app)
        self.person_snapshot_search.setup(self.fastapi_app)
        self.person_flow_search.setup(self.fastapi_app)
        self.person_flow_weight_search.setup(self.fastapi_app)
        self.person_snapshot_image_search.setup(self.fastapi_app)
        self.person_snapshot_answer_search.setup(self.fastapi_app)
        self.person_snapshot_answer_assign.setup(self.fastapi_app)
        self.person_snapshot_answer_delete.setup(self.fastapi_app)
        self.person_snapshot_search_rank.setup(self.fastapi_app)
        self.person_snapshot_search_nearest.setup(self.fastapi_app)
        self.camera_frame_search.setup(self.fastapi_app)
        self.camera_frame_image_search.setup(self.fastapi_app)
        self.person_snapshot_refresh_feature_extract.setup(self.fastapi_app)
        self.person_snapshot_search_query_is_not_junk.setup(self.fastapi_app)
        self.person_snapshot_search_query_is_junk.setup(self.fastapi_app)
        self.person_snapshot_search_gallery_contains_junk.setup(
            self.fastapi_app)
        self.person_snapshot_search_gallery_not_contains_junk.setup(
            self.fastapi_app)
        self.reid_evaluation.setup(self.fastapi_app)
        uvicorn.run(self.fastapi_app, host=self.app_host, port=self.app_port)


if __name__ == "__main__":
    server_app = ServerApp.create(environment=Environment())
    server_app.run()
