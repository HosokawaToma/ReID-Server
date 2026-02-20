"""
カメラフレームのリポジトリ

カメラフレームの検索・件数取得を行う。
"""
from repositories.utils.database import RepositoryUtilDatabase
from repositories.utils.database.query.camera_frame import RepositoryUtilDatabaseQueryCameraFrame
from migration.models.camera_frames import MigrationModelCameraFrame
from domain.id import DomainId
from domain.camera_frame import DomainCameraFrame
from domain.timestamp import DomainTimestamp
from domain.location import DomainLocation
from domain.camera_frame.sequence import DomainCameraFrameSequence
from environment import Environment
from domain.paging import DomainPaging
from repositories.utils.base import RepositoryUtilBase


class RepositoryCameraFrame(RepositoryUtilBase):
    """
    カメラフレームのリポジトリクラス。

    クエリとページングに応じてカメラフレームを検索・件数取得する。
    """

    def __init__(self, database: RepositoryUtilDatabase):
        """
        リポジトリを初期化する。

        :param RepositoryUtilDatabase database: データベースユーティリティ
        """
        self.database = database

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryCameraFrame":
        """
        環境変数からリポジトリインスタンスを生成する。

        :param Environment environment: 環境変数
        :return RepositoryCameraFrame: リポジトリインスタンス
        """
        return cls(
            database=RepositoryUtilDatabase.create(environment),
        )

    def _model_to_domain(self, model: MigrationModelCameraFrame) -> DomainCameraFrame:
        """
        DBモデルをカメラフレームドメインに変換する。

        :param MigrationModelCameraFrame model: カメラフレームのDBモデル
        :return DomainCameraFrame: カメラフレームドメイン
        """
        return DomainCameraFrame(
            id=DomainId(id=model.id),
            location=DomainLocation(
                camera_id=model.camera_id, view_id=model.view_id),
            timestamp=DomainTimestamp(timestamp=model.timestamp),
        )

    def search(
        self,
        paging: DomainPaging,
        query: RepositoryUtilDatabaseQueryCameraFrame | None = None,
    ) -> DomainCameraFrameSequence:
        """
        クエリとページングに応じてカメラフレームを検索する。

        :param DomainPaging paging: ページング
        :param RepositoryUtilDatabaseQueryCameraFrame query: 検索クエリ（Noneの場合は条件なし）
        :return DomainCameraFrameSequence: カメラフレームのシーケンス
        """
        with self.database as session:
            session_query = session.query(MigrationModelCameraFrame)
            if query is not None:
                session_query = query.build(session_query)
            session_query = self._apply_paging(session_query, paging)
            models = session_query.all()
            return DomainCameraFrameSequence(items=[self._model_to_domain(model) for model in models])

    def search_count(
        self,
        query: RepositoryUtilDatabaseQueryCameraFrame | None = None,
    ) -> int:
        """
        クエリに一致するカメラフレームの件数を返す。

        :param RepositoryUtilDatabaseQueryCameraFrame query: 検索クエリ（Noneの場合は全件）
        :return int: 件数
        """
        with self.database as session:
            session_query = session.query(MigrationModelCameraFrame)
            if query is not None:
                session_query = query.build(session_query)
            return session_query.count()
