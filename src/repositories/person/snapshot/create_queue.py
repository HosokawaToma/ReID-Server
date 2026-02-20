"""
人物検出キュー（作成用）のリポジトリ

カメラフレーム画像を人物検出キューに投入・取得する責務を持つ。
Redis・DB・ストレージを利用してキューと永続化を行う。
"""
from repositories.utils.redis import RepositoryUtilRedis
from repositories.utils.redis import RepositoryUtilRedisKey
from repositories.utils.database import RepositoryUtilDatabase
from repositories.utils.storage import RepositoryUtilStorage
from repositories.utils.storage.paths.camera_frame import RepositoryUtilStoragePathCameraFrame
from domain.camera_frame.image import DomainCameraFrameImage
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.image import DomainImage
from migration.models.camera_frames import MigrationModelCameraFrame
from environment import Environment
from error import NotFoundError
from uuid import UUID


class RepositoryPersonSnapshotCreateQueue:
    """
    人物検出キュー（作成用）のリポジトリクラス

    カメラフレーム画像をキューに push/pop し、ストレージ・DB と同期する。
    """

    def __init__(
        self,
        redis: RepositoryUtilRedis,
        database: RepositoryUtilDatabase,
        storage: RepositoryUtilStorage,
    ):
        """
        :param RepositoryUtilRedis redis: Redis ユーティリティ
        :param RepositoryUtilDatabase database: データベースユーティリティ
        :param RepositoryUtilStorage storage: ストレージユーティリティ
        """
        self.redis = redis
        self.database = database
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshotCreateQueue":
        """
        インスタンスを生成する。

        :param Environment environment: 環境設定
        :return RepositoryPersonSnapshotCreateQueue: リポジトリインスタンス
        """
        return cls(
            redis=RepositoryUtilRedis.create(environment),
            database=RepositoryUtilDatabase.create(environment),
            storage=RepositoryUtilStorage.create(environment),
        )

    def _model_to_domain(self, model: MigrationModelCameraFrame, image: DomainImage) -> DomainCameraFrameImage:
        """
        マイグレーションモデルと画像からドメインのカメラフレーム画像を組み立てる。

        :param MigrationModelCameraFrame model: カメラフレームのDBモデル
        :param DomainImage image: 画像ドメイン
        :return DomainCameraFrameImage: カメラフレーム画像ドメイン
        """
        return DomainCameraFrameImage(
            id=DomainId(id=model.id),
            location=DomainLocation(
                camera_id=model.camera_id, view_id=model.view_id),
            timestamp=DomainTimestamp(timestamp=model.timestamp),
            image=image,
        )

    def _domain_to_model(self, domain: DomainCameraFrameImage) -> MigrationModelCameraFrame:
        """
        ドメインのカメラフレーム画像をマイグレーションモデルに変換する。

        :param DomainCameraFrameImage domain: カメラフレーム画像ドメイン
        :return MigrationModelCameraFrame: カメラフレームのDBモデル
        """
        return MigrationModelCameraFrame(
            id=domain.id.id,
            camera_id=domain.location.camera_id,
            view_id=domain.location.view_id,
            timestamp=domain.timestamp.timestamp,
        )

    def push(self, frame_image: DomainCameraFrameImage) -> None:
        """
        画像を人物検出キューに追加します
        キューへの追加が失敗してもストレージとデータベースへの追加は行われます
        :param DomainCameraFrameImage frame_image: 画像
        :raises InternalServerError: 画像のキューへの追加が失敗した場合
        """
        with self.database as session:
            self.storage.save_image(
                image=frame_image.image,
                path=RepositoryUtilStoragePathCameraFrame(
                    id=frame_image.id,
                ),
            )
            session.add(self._domain_to_model(frame_image))
        self.redis.push(
            key=RepositoryUtilRedisKey.PERSON_SNAPSHOT_CREATE,
            value={"id": str(frame_image.id)},
        )

    def pop(self) -> DomainCameraFrameImage:
        """
        人物検出キューから1件取り出し、ストレージ・DBから画像とメタデータを取得して返す。

        :return DomainCameraFrameImage: カメラフレーム画像
        :raises NotFoundError: キューで参照しているIDの画像がDBに存在しない場合
        """
        data = self.redis.dequeue(
            RepositoryUtilRedisKey.PERSON_SNAPSHOT_CREATE)
        with self.database as session:
            query = session.query(MigrationModelCameraFrame)
            query = query.filter(
                MigrationModelCameraFrame.id == UUID(data["id"]))
            model = query.first()
            if model is None:
                raise NotFoundError("画像が見つかりません")
            image = self.storage.search_image(
                path=RepositoryUtilStoragePathCameraFrame(
                    id=DomainId(id=model.id),
                )
            )
            return self._model_to_domain(model, image)
